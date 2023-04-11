import nextcord, os
from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption
from src.classes.anilistClasses import *
from src.classes.defaultFuncs import *

class SlashAni(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #[+] Base For Anilist Commands [+]#
    @slash_command()
    async def anilist(self, interaction: Interaction):
        pass

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] Set Anilist Into Database [+]#
    @anilist.subcommand(name="aniset", description="Set your anilist account!")
    async def anilist_aniset(self, interaction: Interaction, anilist_username: str = SlashOption("anilist_username", description="Your anilist username", required=True)):        
        user = await sqlFunc.sql.fetchval("SELECT anilist_name FROM anilist WHERE discord_id = $1", interaction.user.id)
        anilist = await Functions.User(anilist_username)

        if anilist['errorCode'] != 200:
            return await interaction.send("Seems like there was an error, did you type your anilist name correctly?", ephemeral=True)

        embed = nextcord.Embed(title=anilist['name'], url=anilist['url'], colour=int(os.getenv("COL"), 16))
        embed.set_image(url=anilist['avatar'])

        if user is None:
            await sqlFunc.sql.execute("INSERT INTO anilist(discord_id, discord_name, anilist_name, anilist_id, anilist_url) VALUES ($1, $2, $3, $4, $5)", interaction.user.id, interaction.user.name, anilist['name'], anilist['id'], anilist['url'])
        else:
            await sqlFunc.sql.execute("UPDATE anilist SET discord_name = $1, anilist_name = $2, anilist_id = $3, anilist_url = $4 WHERE discord_id = $5", interaction.user.name, anilist['name'], anilist['id'], anilist['url'], interaction.user.id)
        await interaction.send(embed=embed, ephemeral=True)

    #[+] View User Information [+]#
    @anilist.subcommand(name="user", description="View information about an User")
    async def anilist_user(self, interaction: Interaction, username: str = SlashOption("username", description="Name Of User || KEEP BLANK IF YOU WANT TO VIEW YOURSELF & IN THE DB", required=False)):
        if username == None:
            user = await sqlFunc.sql.fetchval("SELECT anilist_name FROM anilist WHERE discord_id = $1", interaction.user.id)
            if user is None:
                return await interaction.send("Looks like you're not in the database. Please use /aniset to set your account!", ephemeral=True)
        else: user = username

        ani = await Functions.User(user)

        if ani['errorCode'] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?", ephemeral=True)

        embed = nextcord.Embed(title=ani['name'] + ' statistics', url=ani['url'],
        description=f"""
        [**__Anime Information__**]({ani['url']}/animelist)
        `Anime Count    :` {ani['animeCount']}
        `Mean Score     :` {ani['animeMean']}
        `Watch Time     :` {returnTime(ani['animeTime'])}
        `Watched Eps    :` {ani['animeWatch']}

        [**__Manga Information__**]({ani['url']}/mangalist)
        `Manga Count    :` {ani['mangaCount']}
        `Mean Score     :` {ani['mangaMean']}
        `Volumes Read   :` {ani['mangaVolume']}
        `Chapters Read  :` {ani['mangaChapt']}
        
        """,colour=int(os.getenv("COL"), 16))
        embed.set_thumbnail(url=ani['avatar'])
        embed.set_image(url=ani['banner'])
        embed.set_footer(text=f"{ani['id']} | {returnTime(ani['updated'])}")

        await interaction.send(embed=embed)

# _________________________________________________________________________________________________________________________________________________________________ #    

    #[+] View An Anime [+]#
    @anilist.subcommand(name="anime", description="View information about an Anime")
    async def anilist_anime(self, interaction: Interaction, anime_name: str = SlashOption("anime_name", description="Name of the Anime", required=True)):
        members = []; dbMembs = []
    
        try: db = await sqlFunc.sql.fetch("SELECT anilist_name, discord_id FROM anilist") 
        except: db = []

        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                dbMembs.append(db[key]['anilist_name'])

        relation = await Functions.SearchRelations(anime_name, 'ANIME')

        if relation[1][0] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?", ephemeral=True)

        await interaction.send(view=TypeViewer(relation[1], relation[0], dbMembs, 'ANIME'))

    #[+] View An Manga [+]#
    @anilist.subcommand(name="manga", description="View information about an Manga")
    async def anilist_manga(self, interaction: Interaction, manga_name: str = SlashOption("manga_name", description="Name of the Manga", required=True)):
        members = []; dbMembs = []

        try: db = await sqlFunc.sql.fetch("SELECT anilist_name, discord_id FROM anilist") 
        except: db = []
    
        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                dbMembs.append(db[key]['anilist_name'])

        relation = await Functions.SearchRelations(manga_name, 'MANGA')

        if relation[1][0] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?", ephemeral=True)

        await interaction.send(view=TypeViewer(relation[1], relation[0], dbMembs, 'MANGA'))

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] Grab Affinity For Users Within Guild [+]#
    @anilist.subcommand(name="affinity", description="View the affinity for the current guild.")
    async def anilist_affinity(self, interaction: Interaction):
        await interaction.response.defer() # Allows discord to wait longer for the command
        who_used_comm = interaction.user.id; db = await sqlFunc.sql.fetch("SELECT anilist_name, discord_id FROM anilist")
        members = []; dbMembs = []; affinityList = []; usedCommArray = {}

        #Loop through members and remove bots
        for member in interaction.guild.members:
            if member.bot == False:
                members.append(member.id)

        #Check to see if the users within guild are in the database
        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                if db[key]['discord_id'] == who_used_comm:
                    who_used_comm = db[key]['anilist_name']
                else:
                    dbMembs.append(db[key]['anilist_name'])

        #Add a fake user to the end of the list, so once all users have been looped through it wipes the array for more usage
        dbMembs.append('Last User In List')

        # If who_used_comm variable wasn't updated, we know the user who used this command isn't in the database
        if who_used_comm == interaction.user.id:
            return await interaction.send("You have not set your anilist with the bot. Please use /anilist aniset", ephemeral=True)

        #[+] Create User Who Used Command First, To Avoid Errors [+]#
        # --> THIS IS A MUST OTHERWISE IT JUST BREAKS IDK WHY
        usedCommOwner = await Functions.FirstAni(who_used_comm)

        #Loop through members within the database and calculate their affinity
        for member in dbMembs:
            affinity = await Functions.Affinity(who_used_comm, member)
            affinityList.append(f"**{affinity['affinity']}%** with **[{affinity['name']}]({affinity['url']})** - [*{affinity['shares']} media shares*]")

        # Well, this works and doesn't (negatives show up at the top)
        affinityList.sort(key=natural_keys); affinityList.reverse()

        #Create and send embed of all members
        embed = nextcord.Embed(title=f"{usedCommOwner['name']}' affinity", url=usedCommOwner['url'], 
        description='\n'.join(affinityList), colour=int(os.getenv("COL"), 16))

        embed.set_thumbnail(url=usedCommOwner['avatar'])
        await interaction.send(embed=embed)

    #[+] Information About Staff Members [+]#
    @anilist.subcommand(name="staff", description="View information about a staff member")
    async def anilist_staff(self, interaction: Interaction, staff_name: str = SlashOption("staff_name", description="Name of staff member", required=True)):
        pass

# _________________________________________________________________________________________________________________________________________________________________ #