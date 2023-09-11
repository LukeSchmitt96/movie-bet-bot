import discord

from movie_bet_bot.utils.images import html_to_image


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
        print("Running Help Command")
        # create a new embed
        embed: discord.Embed = discord.Embed(description="List of all commands:", color=0x000000)
        for command in bot.commands:
            # add the embed field for the command
            embed.add_field(name=command["name"], value=command["description"], inline=False)
        # send the embed
        print("Sending Help Embed")
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
        print("Running Standings Command")
        error: bool = True
        if bot.contest is not None:
            # update the standings if update_standings_first is true
            if update_standings_first:
                print("Updating Standings")
                update_standings_first = await bot.contest.update()
            # get the image of the standings
            (image_html, image_size) = bot.contest.to_standings_image_html(
                update_standings_first, show_hours_watched
            )
            # create a new discord.File from html_to_image-provided filepath
            file = discord.File(
                html_to_image(html=image_html, out="update_image.png", size=image_size)
            )
            if file is not None:
                # sends the file
                print("Sending Standings File")
                error = False
                await interaction.followup.send(file=file)
        if error:
            print("Could not get standings")
            await interaction.followup.send("Could not get standings")

    # add a command to the list of commands
    bot.add_command(name, description)


def create_average_watchtimes(bot):
    """
    Create the average watchtime command.

    :param bot: client.MovieBetBot to add average watchtime command to
    """

    # name of the average watchtime command
    name = "avg_watchtime"

    # description of the average watchtime command
    description = "Get the average watchtimes."

    @bot.command_tree.command(name=name, description=description)
    async def average_watchtimes(
        interaction: discord.Interaction,
    ):
        """Do average watchtime command callback"""
        print("Running Average Watchtimes Command")
        await interaction.response.defer()
        error: bool = True
        if bot.contest is not None:
            # get the image of the average watchtimes
            (image_html, image_size) = bot.contest.to_avg_watchtimes_image_html()
            # create a new discord.File from html_to_image-provided filepath
            file = discord.File(
                html_to_image(html=image_html, out="avg_watchtimes.png", size=image_size)
            )
            if file is not None:
                # sends the file
                print("Sending Average Watchtimes File")
                error = False
                await interaction.followup.send(file=file)
        if error:
            print("Could not get average watchtimes")
            await interaction.followup.send("Could not get average watchtimes")

    # add a command to the list of commands
    bot.add_command(name, description)


def create_unique_films(bot):
    """
    Create the unique films command.

    :param bot: client.MovieBetBot to add unique films command to
    """

    # name of the unique films command
    name = "unique_films"

    # description of the average watchtime command
    description = "Get the number of unique films for each member."

    @bot.command_tree.command(name=name, description=description)
    async def unique_films(
        interaction: discord.Interaction,
    ):
        """Do unique films command callback"""
        print("Running Unique Films Command")
        await interaction.response.defer()
        error: bool = True
        if bot.contest is not None:
            # get the image of the unique films
            (image_html, image_size) = bot.contest.to_unique_films_image_html()
            # create a new discord.File from html_to_image-provided filepath
            file = discord.File(
                html_to_image(html=image_html, out="unique_films.png", size=image_size)
            )
            if file is not None:
                # sends the file
                print("Sending Unique Films File")
                error = False
                await interaction.followup.send(file=file)
        if error:
            print("Could not get unique films")
            await interaction.followup.send("Could not get unique films")

    # add a command to the list of commands
    bot.add_command(name, description)
