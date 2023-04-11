import nextcord, requests
from nextcord.ext import commands
from src.classes.defaultFuncs import *
from nextcord import slash_command, Interaction, SlashOption

url = 'https://api.henrikdev.xyz/'

class SlashVal(commands.Cog):
    def __init__(self, client):
        self.client = client

# _________________________________________________________________________________________________________________________________________________________________ #

    #[+] Base For User Commands [+]#
    @slash_command(guild_ids=[1066884123353939978])
    async def valorant(self, interaction: Interaction):
        pass

# _________________________________________________________________________________________________________________________________________________________________ #

    @valorant.subcommand(name="set", description="Set your valorant account")
    async def valo_set(self, interaction: Interaction,
            val_name: str = SlashOption("username", "Example: tomos", required=True),
            val_tag: str = SlashOption("tag", "Example: #gamin", required=True),
            region: str = SlashOption("region", "Example: EU", required=True, choices=['EU', 'NA', 'AP', 'KR'])):
        
        if '#' in val_tag:
            val_tag = val_tag.replace('#', '')

        user = await sqlFunc.sql.fetchval("SELECT username FROM valorant WHERE discord_id = $1", interaction.user.id)
        if user is None:
            await sqlFunc.sql.execute("INSERT INTO valorant(discord_id, username, tag, region) VALUES ($1, $2, $3, $4)", interaction.user.id, val_name, val_tag, region.lower())
        else:
            await sqlFunc.sql.execute("UPDATE anilist SET username = $1, tag = $2, region = $3 WHERE discord_id = $4", val_name, val_tag, region.lower(), interaction.user.id)
        await interaction.send(f"You have now linked your account to **{val_name}#{val_tag}**.")

# _________________________________________________________________________________________________________________________________________________________________ #

    @valorant.subcommand(name="account", description="View your valorant account information")
    async def valo_acc(self, interaction: Interaction, user: nextcord.Member = SlashOption("user", "View a users information", required=False)):
        if user == None:
            user = interaction.user.id

        db = await sqlFunc.sql.fetch("SELECT username, tag, region FROM valorant WHERE discord_id = $1", user)
        user = db[0]['username']
        tag = db[0]['tag']
        region = db[0]['region']

        user_req = requests.get(url+f'valorant/v1/account/{user}/{tag}').json()
        rank_req = requests.get(url+f'valorant/v1/mmr/{region}/{user}/{tag}').json()
        data = user_req['data']
        rData = rank_req['data']

        embed = nextcord.Embed(title=f"{data['name']}#{data['tag']}", description=f"`Rank    :` **{rData['currenttierpatched']}**\n`Tier    :`**{rData['currenttier']}**\n`Region  :` **{str(data['region']).upper()}**"
                               + f"\n`Level   :` **{data['account_level']}**\n`PUUID   :` **{data['puuid']}**")
        embed.set_thumbnail(url=rData['images']['large'])
        embed.set_image(url=data['card']['wide'])
        await interaction.send(embed=embed)

# _________________________________________________________________________________________________________________________________________________________________ #

    @valorant.subcommand(name="history", description="View your match history")
    async def valo_history(self, interaction: Interaction, 
        user: nextcord.Member = SlashOption("user", "View someones history", required=False),
        filter: str = SlashOption("mode", "Check a specific gamemode, leave blank if not", choices=["escalation", "spikerush", "deathmatch", "competitive", "unrated", "replication"], required=False)):
        if user == None:
            user = interaction.user.id
        
        db = await sqlFunc.sql.fetch("SELECT username, tag, region FROM valorant WHERE discord_id = $1", user)
        user = db[0]['username']
        tag = db[0]['tag']
        region = db[0]['region']
        url = f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{user}/{tag}"
        
        if filter != None:
            url = url + f"?filter={filter}"
        
        maps, players = [], []

        hist_req = requests.get(url).json()
        data = hist_req['data']

        # _________________________________________________________________________________________________________________________________________________________________ #

        #HARD CODE IT IN
        map1 = data[0]['metadata']['map']
        pData = data[0]['players']['all_players'][0]

        #[+] Person who used command [+]#
        ownerName = pData['name']
        ownerTag = pData['tag']
        ownerTeam = pData['team']

        clamp = len(pData)-1
        totalClamp = max([clamp])
        while totalClamp >= 0:
            if clamp >= 0:
                print(pData[clamp])
                clamp -= 1
            totalClamp -= 1