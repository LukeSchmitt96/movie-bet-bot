from typing import Any, List

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from movie_bet_bot.models.commands import create_help, create_standings
from movie_bet_bot.models.logger import print
from movie_bet_bot.models.movies import movies
from movie_bet_bot.utils import constants

INTENTS = discord.Intents.default()


class MovieBetBot(discord.Client):

    # bot's contest
    contest: movies.Contest

    # channel bot will post in
    channel: discord.Thread

    # Discord's command tree. This is used to create and sync commands
    command_tree: discord.app_commands.CommandTree

    # list of bot's commands
    commands: List[discord.app_commands.Command] = []

    def __init__(self, contest: movies.Contest, **options: Any) -> None:
        super().__init__(intents=INTENTS, **options)
        self.contest = contest
        # set Discord's command tree. This is used to create and sync commands
        self.command_tree = discord.app_commands.CommandTree(self)
        self.command_setup()

    def run(self) -> None:
        """Run the client with API token."""
        super().run(constants.TOKEN)

    async def on_ready(self) -> None:
        """Do hooks to be completed after bot has connected to Discord's server."""
        print(f"Logged in as {self.user}")
        # get the channel with the channel ID
        self.channel = self.get_channel(constants.CHANNEL_ID)
        # set up task look
        self.loop.create_task(self.task_setup())
        await self.sync_commands()
        # update standings
        await self.contest_message_task()

    async def send_message(self, msg: str = None, filepath: str = None) -> None:
        """
        Send given message and file to bot's channel.

        :param msg: message to send to channel
        :param filepath: absolute path to file to send to channel
        """
        # if given filepath, create discord.File from it
        file = discord.File(filepath) if filepath is not None else None
        # send message, file to channel
        await self.channel.send(msg, file=file)

    async def contest_message_task(self) -> None:
        """Update contest and send its update image."""
        if await self.contest.update():
            await self.send_message(filepath=self.contest.to_image())

    async def task_setup(self) -> None:
        """Set up tasks."""
        # create async scheduler
        scheduler = AsyncIOScheduler()
        # add task to update contest and send update image hourly
        scheduler.add_job(self.contest_message_task, "cron", hour="*")
        # start scheduler
        scheduler.start()

    def clear_commands(self) -> None:
        """Clear all commands from Discord's servers."""
        self.command_tree.clear_commands(guild=None)

    async def sync_commands(self):
        """Sync commands to Discord's servers."""
        await self.command_tree.sync()

    def create_commands(self) -> None:
        """Create all commands."""
        # create help command
        create_help(self)
        # create standings command
        create_standings(self)

    def add_command(self, name: str, description: str) -> None:
        """Add a command to the list of commands.

        :param name: name of command to add
        :description: description of command to add
        """
        # check if command already exists in command tree
        command: discord.app_commands.Command = self.command_tree.get_command(name)
        if command is not None:
            # add the command to the list of commands if it wasn't already
            command = {
                "name": name,
                "description": description,
                "callback": command.callback,
            }
            self.commands.append(command)

    def command_setup(self) -> None:
        """Set up commands."""
        # clear all commands from Discord's servers
        self.clear_commands()
        # create all commands
        self.create_commands()
