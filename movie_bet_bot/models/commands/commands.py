import discord
from movie_bet_bot.models.logger.logger import Logger

# creates the help command. Always add this command last
def create_help(bot):
    # sets the name of the command
    name = "help"
    # sets the description of the command
    description: str = "Shows a list of all commands."

    # creates the help command
    @bot.command_tree.command(name = name, description = description)
    # the function that is called when the command is executed
    async def help(interaction: discord.Interaction):
        Logger.info("Running Help Command")
        # creates a new embed
        embed: discord.Embed = discord.Embed(description = "List of all commands:", colour = 0x000000)
        for command in bot.commands:
            # adds the embed field for the command
            embed.add_field(
                name = command.name, value = command.description, inline = False
            )
        # sends the embed
        Logger.info("Sending Help Embed")
        await interaction.response.send_message(embed = embed)
    # adds a command to the list of commands
    bot.add_command(name, description)

# creates the standings command
def create_standings(bot):
    # sets the name of the command
    name = "standings"
    # sets the description of the command
    description = "Get the competition standings.aa"

    # creates the help command
    @bot.command_tree.command(name = name, description = description)
    # the function that is called when the command is executed
    async def standings(interaction: discord.Interaction, update_standings_first: bool = False, show_hours_watched: bool = False):
        Logger.info("Running Standings Command")
        if bot.contest is not None:
            # updates the standings if update_standings_first is true
            if update_standings_first:
                Logger.info("Updating Standings")
                update_standings_first = await bot.bot.contest.update()
            # gets the image of the standings
            image = bot.contest.to_image(update_standings_first, show_hours_watched)
            if image is not None and len(image) > 0:
                filepath = image[0]
                if filepath is not None:
                    # creates a new file
                    file = discord.File(filepath)
                    if file is not None:
                        # sends the file
                        Logger.info("Sending Standings File")
                        await interaction.response.send_message(file = file)

    # adds a command to the list of commands
    bot.add_command(name, description)
