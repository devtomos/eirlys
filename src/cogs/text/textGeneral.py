import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction
from src.classes.defaultClasses import *
from src.classes.defaultFuncs import *


class TextGeneral(commands.Cog):
    def __init__(self, client):
        self.client = client

    # _________________________________________________________________________________________________________________________________________________________________ #

    # [+] Check Latency/Uptime [+]#
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"`Discord Latency    :` {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Not Finished")

    # _________________________________________________________________________________________________________________________________________________________________ #

    # [+] View An Avatar [+]#
    @commands.command(aliases=['avi', 'av', 'pfp'])
    async def avatar(self, interaction: Interaction, member: nextcord.Member = None):
        # [+] In Case User Wants Their Own Avatar [+]#
        member = member if not member else member
        defaultAvi = None

        try:
            defaultAvi = member.avatar.url
        except:
            defaultAvi = member.default_avatar.url

        embed = nextcord.Embed(colour=int(os.getenv("COL"), 16))
        embed.set_image(url=defaultAvi)

        if member.guild_avatar is None:
            await interaction.send(embed=embed)
        else:
            await interaction.send(embed=embed, view=AvatarViewer(defaultAvi, member.guild_avatar.url))

    @commands.command()
    async def banner(self, interaction: Interaction, member: nextcord.Member = None):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            logging.critical(error)
            embed = nextcord.Embed(title="Error :x:", description=f"```py\n{error}\n```", colour=nextcord.Colour.red())
            await ctx.send(embed=embed)
