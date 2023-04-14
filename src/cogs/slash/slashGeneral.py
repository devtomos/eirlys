from datetime import datetime

from nextcord import slash_command, Interaction
from nextcord.ext import commands

from src.classes.defaultClasses import *
from src.classes.defaultFuncs import *


class SlashGeneral(commands.Cog):
    def __init__(self, client):
        self.client = client

    # _________________________________________________________________________________________________________________________________________________________________ #

    # [+] Check Latency/Uptime [+]#
    @slash_command(name="ping", description="Check latency for Shards and Discord.")
    async def ping(self, interaction: Interaction):
        shards = []
        for i in range(0, 3):
            shards.append(f"`Shard {i}     :` {round(self.client.get_shard(i).latency * 1000)}ms")

        embed = nextcord.Embed(description=f"`Discord Latency     :` {round(self.client.latency * 1000)}ms\n\n" + '\n'.join(shards), colour=int(os.getenv("COL"), 16))
        await interaction.send(embed=embed)

    # [+] Help Command [+]#
    @slash_command(name="help", description="Need help? Use this command to figure out how to use the bot.")
    async def help(self, interaction: Interaction):
        await interaction.send("Not Finished")

    # _________________________________________________________________________________________________________________________________________________________________ #

    # [+] Base For User Commands [+]#
    @slash_command()
    async def user(self, interaction: Interaction):
        pass

    # [+] View User Avatar [+]#
    @user.subcommand(name="avatar", description="view yours or someones avatar!")
    async def user_avatar(self, interaction: Interaction, member: nextcord.Member):
        defaultAvi = None

        try:
            defaultAvi = member.avatar.url
        except:
            defaultAvi = member.default_avatar.url

        embed = nextcord.Embed(colour=int(os.getenv("COL"), 16))
        embed.set_image(url=defaultAvi)
        if member.guild_avatar is None:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, view=AvatarViewer(defaultAvi, member.guild_avatar.url))

    # [+] View User Banner [+]#
    @user.subcommand(name="banner", description="view yours or someones banner!")
    async def user_banner(self, interaction: Interaction, member: nextcord.Member):
        member = await self.client.fetch_user(member.id)

        try:
            banner = member.banner.url
        except:
            return await interaction.send(f"`{member.display_name}` has no banner or has a guild banner.")

        embed = nextcord.Embed(colour=int(os.getenv("COL"), 16))
        embed.set_image(url=banner)
        await interaction.response.send_message(embed=embed)

    # [+] View User Information [+]#
    @user.subcommand(name="info", description="view information about yourself or someone!")
    async def user_info(self, interaction: Interaction, member: nextcord.Member):
        fetchMember = await self.client.fetch_user(member.id)
        activiesList, bannerURL, avatarURL = [], None, None

        grabRoles = [role for role in member.roles]
        roles = ', '.join([role.mention for role in grabRoles])
        status = str(member.status).capitalize()
        activies = member.activities

        if fetchMember.banner is None:
            bannerURL = "https://i.imgur.com/FdFIkxG.png"
        else:
            bannerURL = fetchMember.banner.url

        if member.avatar is None:
            avatarURL = member.default_avatar.url
        else:
            avatarURL = member.avatar.url

        if status == "Dnd":
            status = "Do not Disturb"  # I do not like DND

        activityClamp = len(activies) - 1
        totalClamp = max([activityClamp])
        while totalClamp >= 0:
            if activityClamp >= 0:
                activiesList.append(f"> **{activies[activityClamp].name}**")
                activityClamp -= 1
            totalClamp -= 1

        for activity in activiesList:
            if activity == '> **None**':
                activiesList.remove(activity)

        if activiesList == []:
            activiesList.append('> **No Activities**')

        infoParse = [
            '**_Information_**\n', f'`Status    :` **{status}**\n', f'`Activity  :`\n' + "\n".join(activiesList) + '\n',
            f'`Created   :`\n> <t:{int(member.created_at.timestamp())}:f>\n> <t:{int(member.created_at.timestamp())}:R>\n',
            f'`Joined    :`\n> <t:{int(member.joined_at.timestamp())}:f>\n> <t:{int(member.joined_at.timestamp())}:R>\n',
            '\n**_Roles_**\n', roles]

        embed = nextcord.Embed(title=f"{member.name}#{member.discriminator}", description=''.join(infoParse),
                               colour=int(os.getenv("COL"), 16))
        embed.set_image(url=bannerURL)
        embed.set_thumbnail(url=avatarURL)
        embed.set_footer(text=f'ID: {member.id} | {datetime.now().strftime("%a, %#d %b %Y, %I:%M %p")}')
        await interaction.response.send_message(embed=embed)

    # _________________________________________________________________________________________________________________________________________________________________ #

    # [+] Base For Guilds [+]#
    @slash_command()
    async def guild(self, interaction: Interaction):
        pass

    # [+] View Guild Avatar [+]#
    @guild.subcommand(name="avatar", description="The current guild's avatar")
    async def guild_avatar(self, interaction: Interaction):
        guild = interaction.user.guild

        if guild.icon is None:
            return await interaction.response.send_message(f"`{guild.name}` has no avatar")

        embed = nextcord.Embed(colour=int(os.getenv("COL"), 16))
        embed.set_image(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)

    # [+] View Guild Information [+]#
    @guild.subcommand(name="info", description="Information about the current guild")
    async def guild_info(self, interaction: Interaction):
        guild = interaction.user.guild
        channels, members, bots = [], [], []

        for member in guild.members:
            if member.bot == True:
                bots.append(member)
            else:
                members.append(member)

        for channel in guild.channels:
            if channel.category:
                channels.append(channel)

        grabRoles = [role for role in guild.roles]
        guildRoles = ', '.join([role.mention for role in grabRoles])
        guildBanner = guild.banner

        try:
            guildBanner = guildBanner.url  # Will just break if no try: except:
        except:
            guildBanner = "https://i.imgur.com/FdFIkxG.png"

        guildInfo = [
            '**_Guild Information_**\n',
            f'`Owner     :` **{guild.owner}**\n', f'`Emojis    :` **{len(guild.emojis)}**\n',
            f'`Channels  :` **{len(channels)}**\n', f'`Roles     :` **{len(guild.roles) - 1}**\n',
            f'`Members   :` **{len(members)}**\n', f'`Bots      :` **{len(bots)}**\n',
            f'`Creation  :`\n> <t:{int(guild.created_at.timestamp())}:f>\n> <t:{int(guild.created_at.timestamp())}:R>\n\n',
            f'**_Roles_**\n', guildRoles]

        guildEmbed = nextcord.Embed(title=guild.name, description=' '.join(guildInfo), colour=int(os.getenv("COL"), 16))
        guildEmbed.set_image(url=guildBanner)
        guildEmbed.set_thumbnail(url=guild.icon)
        guildEmbed.set_footer(text=f'ID: {guild.id} | {datetime.now().strftime("%a, %#d %b %Y, %I:%M %p")}')
        await interaction.response.send_message(embed=guildEmbed)

# _________________________________________________________________________________________________________________________________________________________________ #

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction, error):
        logging.critical(error)
        #command = interaction.app_command
        ctx = interaction.context

        embed = nextcord.Embed(title="Error :x:", description=f"```py\n{error}\n```", colour=nextcord.Colour.red())
        await ctx.send(embed=embed)
