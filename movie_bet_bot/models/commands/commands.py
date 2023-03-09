import discord
from movie_bet_bot.models.logger.logger import Logger


def create_help(bot: discord.Client):
    """
    Create the help command for the given bot.

    :param bot: discord.Client to add help command to
    """

    # name of the help command
    name = "help"

    # description of the help command
    description: str = "Shows a list of all commands."

    @bot.command_tree.command(name=name, description=description)
    async def help(interaction: discord.Interaction):
        """Do help command callback."""
        Logger.info("Running Help Command")
        # create a new embed
        embed: discord.Embed = discord.Embed(description="List of all commands:", color=0x000000)
        for command in bot.commands:
            # add the embed field for the command
            embed.add_field(name=command["name"], value=command["description"], inline=False)
        # send the embed
        Logger.info("Sending Help Embed")
        await interaction.response.send_message(embed=embed)

    # add a command to the list of commands
    bot.add_command(name, description)


def create_standings(bot):
    """
    Create the standings command.

    :param bot: discord.Client to add standings command to
    """

    # name of the standings command
    name = "standings"

    # description of the standings command
    description = "Get the competition standings."

    @bot.command_tree.command(name=name, description=description)
    async def standings(
        interaction: discord.Interaction,
        update_standings_first: bool = False,
        show_hours_watched: bool = False,
    ):
        """Do standings command callback"""
        Logger.info("Running Standings Command")
        error: bool = True
        if bot.contest is not None:
            # update the standings if update_standings_first is true
            if update_standings_first:
                Logger.info("Updating Standings")
                update_standings_first = await bot.bot.contest.update()
            # get the image of the standings
            filepath = bot.contest.to_image(update_standings_first, show_hours_watched)
            # create a new discord.File from filepath
            file = discord.File(filepath)
            if file is not None:
                # sends the file
                Logger.info("Sending Standings File")
                error = False
                await interaction.response.send_message(file=file)
        if error:
            Logger.info("Could not get standings")
            await interaction.response.send_message("Could not get standings")

    # add a command to the list of commands
    bot.add_command(name, description)
