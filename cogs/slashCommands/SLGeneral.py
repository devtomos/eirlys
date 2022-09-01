import nextcord, pprint, asyncpraw, asyncio
from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption, SelectOption
from datetime import datetime
from classes.generalClasses import *
from cogs.normalCommands.general import RunTimes

async def SLGeneralDB(connect):
    global sql
    sql = connect
    return

class SLGeneral(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = asyncpraw.Reddit(client_id=col['Reddit']['ID'], client_secret=col['Reddit']['CLIENT_SECRET'], user_agent=col['Reddit']['USER_AGENT'])
    
    #|----------Check Latency----------|
    @slash_command("ping", "View Latency and Uptime for the Bot.")
    async def ping(self, interaction: Interaction):
        await interaction.send(f"`🏓 Ping     :`\n> Client - {round(self.client.latency * 1000)}ms\n> Uptime - {returnTime(RunTimes.timer)}")

    @slash_command("help", "Help Command!")
    async def help(self, interaction: Interaction):
        await interaction.send("Slash commands are different, will figure how to find them soon.")

    #|----------View User Avatar(s)----------|
    @slash_command("avatar", "View Global and Guild avatar!")
    async def avatar(self, interaction: Interaction, member: nextcord.Member):
        try: guildAvatar = member.guild_avatar.url
        except: guildAvatar = None

        try: memberAvatar = member.avatar.url
        except: memberAvatar = member.default_avatar.url

        embed = nextcord.Embed(colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=memberAvatar)

        if guildAvatar == None:
            await interaction.send(embed=embed)
        else:
            await interaction.send(embed=embed, view=AvatarViewer(memberAvatar, guildAvatar))

    #|----------View User Banner----------|
    @slash_command("banner", "View your own or someones banner!")
    async def banner(self, interaction: Interaction, member: nextcord.Member):
        member = await self.client.fetch_user(member.id)
        try: member.banner.url
        except: return await interaction.send(f"{member.display_name} has no banner. (Cannot fetch guild banners if that's what you're after.)")

        embed = nextcord.Embed(colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=member.banner.url)
        await interaction.send(embed=embed)

    #|----------View User Information----------|
    @slash_command("info", "View information about someone or yourself!")
    async def info(self, interaction: Interaction, member: nextcord.Member):
        fetchMember = await self.client.fetch_user(member.id)
        activiesList = []

        grabRoles = [role for role in member.roles]
        roles = ', '.join([role.mention for role in grabRoles])
        status = str(member.status).capitalize()
        activies = member.activities
        joined = int(member.joined_at.timestamp())
        created = int(member.created_at.timestamp())

        try: banner = str(fetchMember.banner.url)
        except: banner = "https://i.imgur.com/FdFIkxG.png"

        try: avatar = member.avatar.url
        except: avatar = member.default_avatar.url
        
        if status == "Dnd":
            status = "Do not Disturb" #I do not like DND

        activityClamp = len(activies)-1
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
            f'`Created   :`\n> <t:{created}:f>\n> <t:{created}:R>\n', f'`Joined    :`\n> <t:{joined}:f>\n> <t:{joined}:R>\n', '\n**_Roles_**\n', roles]

        embed = nextcord.Embed(title=f"{member.name}#{member.discriminator}", description=''.join(infoParse), colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=banner)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text=f'ID: {member.id} | {datetime.now().strftime("%a, %#d %b %Y, %I:%M %p")}')
        await interaction.send(embed=embed)

    #|----------View Guild Information----------|
    @slash_command("guild_info", "View Information about the current guild.")
    async def guildinfo(self, interaction: Interaction):
        guild = interaction.guild
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
        guildName = guild.name
        guildOwner = guild.owner
        guildAvatar = guild.icon
        guildBanner = guild.banner
        guildCreation = int(guild.created_at.timestamp())
        guildMembers = len(members)
        guildRoleLen = len(guild.roles)-1 #-1 Because @everyone gets added on
        guildChannels = len(channels)
        guildEmojis = len(guild.emojis)
        guildBots = len(bots)

        try: guildBanner = guildBanner.url #Will just break if no try: except:
        except: guildBanner = "https://i.imgur.com/FdFIkxG.png"

        guildInfo = [
            '**_Guild Information_**\n',
            f'`Owner     :` **{guildOwner}**\n', f'`Emojis    :` **{guildEmojis}**\n',
            f'`Channels  :` **{guildChannels}**\n', f'`Roles     :` **{guildRoleLen}**\n',
            f'`Members   :` **{guildMembers}**\n', f'`Bots      :` **{guildBots}**\n',
            f'`Creation  :`\n> <t:{guildCreation}:f>\n> <t:{guildCreation}:R>\n\n',
            f'**_Roles_**\n', guildRoles]

        guildEmbed = nextcord.Embed(title=guildName, description=' '.join(guildInfo), colour=int(col['Miumi']['Colour'], 16) + 0x200)
        guildEmbed.set_image(url=guildBanner)
        guildEmbed.set_thumbnail(url=guildAvatar)
        guildEmbed.set_footer(text=f'ID: {guild.id} | {datetime.now().strftime("%a, %#d %b %Y, %I:%M %p")}')
        await interaction.send(embed=guildEmbed)