import os
from typing import Any

import discord
from discord.ext import tasks

from movie_bet_bot.models.movies import Contest

TOKEN: str = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

INTENTS = discord.Intents.default()


class MovieBetBot(discord.Client):

    contest: Contest
    guild: discord.Guild
    channel: discord.Thread
    db_path: str = os.getenv("DB_PATH")

    def __init__(self, contest: Contest, **options: Any) -> None:
        super().__init__(intents=INTENTS, **options)
        self.contest = contest

    def run(self):
        super().run(TOKEN)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.guild = self.get_guild(GUILD_ID)
        self.channel = self.guild.get_channel_or_thread(CHANNEL_ID)
        self.contest_message_task.start()

    async def send_message(self, msg: str = None, filepath: str = None):
        file = discord.File(filepath) if filepath is not None else None
        await self.channel.send(msg, file=file)

    @tasks.loop(minutes=60.0)  # TODO: set this from config
    async def contest_message_task(self) -> None:
        if await self.contest.update():
            self.contest.update_standings()
            await self.send_message(
                filepath=self.contest.to_image()[0],
            )
