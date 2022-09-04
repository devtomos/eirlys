import nextcord
from nextcord.ext import commands

class ErrorHandlers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, commands.CommandNotFound):
            pass #Testing purposes || It worked