import nextcord, random, asyncio
from nextcord.ext import commands
from datetime import datetime
from classes.generalClasses import *
from nextcord import SelectOption
timer = 0

async def RunTimes(client):
    global timer
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(1)
        timer = timer + 1
        RunTimes.timer = timer

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    #|----------Check Latency----------|
    @commands.command()
    async def ping(self, ctx):
        global timer
        await ctx.send(f"`🏓 Ping     :`\n> Client - {round(self.client.latency * 1000)}ms\n> Uptime - {returnTime(timer)}")

    #|----------Custom Help Command----------|
    @commands.command()
    async def help(self, interaction: nextcord.Interaction, commandName = None):
        if commandName == None:
            cogDict, cogs = {}, []
            for command in self.client.commands:
                if command.cog.qualified_name not in cogDict:
                    cogDict[command.cog.qualified_name] = []
                    cogs.append(SelectOption(label=f"{command.cog.qualified_name}"))

                cogDict[command.cog.qualified_name].append(f'> **{str(command.name).capitalize()}**')
            await interaction.send(view=HelpView(cogDict, cogs))
        else:
            pass

    #|----------View User Avatar(s)----------|
    @commands.command(aliases=['ava'])
    async def avatar(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        member = interaction.author if not member else member
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
    @commands.command()
    async def banner(self, ctx, member: nextcord.Member = None):
        member = ctx.author if not member else member
        try: member.banner.url
        except: return await ctx.send(f"{member.display_name} has no banner. (Cannot fetch guild banners if that's what you're after.)")

        embed = nextcord.Embed(colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=member.banner.url)
        await ctx.send(embed=embed)

    #|----------View Guild Avatar----------|
    @commands.command(aliases=['guildava', 'serveravatar', 'serverava'])
    async def guildAvatar(self, ctx):
        guild = ctx.guild
        embed = nextcord.Embed(colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=guild.icon)
        await ctx.send(embed=embed)

    #|----------View User Information----------|
    @commands.command(aliases=['userinfo', 'infouser', 'information'])
    async def info(self, ctx, member: nextcord.Member = None):
        member = ctx.author if not member else member
        try: fetchMember = await self.client.fetch_member(member.id)
        except : fetchMember = None
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
        await ctx.send(embed=embed)

    #|----------View Guild Information----------|
    @commands.command(aliases=['guildinfo', 'serverinformation', 'guildinformation'])
    async def serverinfo(self, ctx):
        guild = ctx.guild
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
        await ctx.send(embed=guildEmbed)

    #|----------Listening for messages----------|
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == '<@795916241193140244>':
            await message.channel.send(f"Prefix is `{self.client.command_prefix}`")

        if 'amq' in message.content:
            await message.channel.send(random.choice(col['AMQ']))