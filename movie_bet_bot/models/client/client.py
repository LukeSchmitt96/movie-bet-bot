from typing import Any
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from movie_bet_bot.models.commands.commands import create_help, create_standings
from movie_bet_bot.models.movies import movies
from movie_bet_bot.utils import constants
from movie_bet_bot.models.logger.logger import print

INTENTS = discord.Intents.default()


class MovieBetBot(discord.Client):

    contest: movies.Contest
    # guild: discord.Guild
    channel: discord.Thread
    # discords command tree. This is used to create and sync commands
    command_tree: discord.app_commands.CommandTree
    # list of created commands
    commands: list[any] = []

    def __init__(self, contest: movies.Contest, **options: Any) -> None:
        super().__init__(intents=INTENTS, **options)
        self.contest = contest
        # set discords command tree. This is used to create and sync commands
        self.command_tree = discord.app_commands.CommandTree(self)
        self.command_setup()

    def run(self):
        super().run(constants.TOKEN)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        # self.guild = self.get_guild(constants.GUILD_ID)
        # self.channel = self.guild.get_channel_or_thread(constants.CHANNEL_ID)
        # get the channel from the list of channels the bot is in
        self.channel = self.get_channel(constants.CHANNEL_ID)
        self.loop.create_task(self.task_setup())
        await self.sync_commands()
        # update standings
        await self.contest_message_task()

    async def send_message(self, msg: str = None, filepath: str = None):
        file = discord.File(filepath) if filepath is not None else None
        await self.channel.send(msg, file=file)

    async def contest_message_task(self) -> None:
        if await self.contest.update():
            await self.send_message(filepath=self.contest.to_image()[0])

    async def task_setup(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.contest_message_task, "cron", hour="*")
        scheduler.start()

    # clears all commands from discords servers
    def clear_commands(self):
        self.command_tree.clear_commands(guild=None)

    # syncs all commands to discords servers
    async def sync_commands(self):
        await self.command_tree.sync()

    # creates all commands
    def create_commands(self):
        # creates the help command
        create_help(self)
        # creates the standings command
        create_standings(self)

    # adds a command to the list of commands
    def add_command(self, name: str, description: str):
        # gets the command from discords command tree
        command: discord.app_commands.Command = self.command_tree.get_command(name)
        if command is not None:
            # adds the command to the list of commands
            command = {
                "name": name,
                "description": description,
                "callback": command.callback,
            }
            self.commands.append(command)

    # command setup
    def command_setup(self):
        # clear all commands from discords servers
        self.clear_commands()
        # create all commands
        self.create_commands()
