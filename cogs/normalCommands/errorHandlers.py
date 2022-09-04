import nextcord
from nextcord.ext import commands
from classes.anilistClasses import *

class ErrorHandlers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.CommandNotFound):
            return #People could type ... etc, it'll just clutter up the logs.
        else:
            embed = nextcord.Embed(description=f"```diff\n- An Error Has Occured!\n\n{error}\n\n- Alert the owner of the bot if this error continues.\n```", colour=int(col['Miumi']['Colour'], 16) + 0x200)
            await interaction.send(embed=embed)
        