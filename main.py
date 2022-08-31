import nextcord, json, asyncpg, asyncio
from nextcord.ext import commands

#|----------TODO List----------|

# Add Airing Schedule back to .anime
# Error handlers to normal commands

#|----------Normal Commands----------|
from cogs.normalCommands.general import General, GeneralDB, RunTimes
from cogs.normalCommands.anilist import Anilist, AnilistDB

#|----------Cog and DB Dicts----------|
cogs = {General: True, Anilist: True}
DBs = {AnilistDB: True, GeneralDB: True}

#|----------Setting Client and Token----------|
client = commands.Bot(command_prefix=".", help_command=None, intents=nextcord.Intents.all(), case_insensitive=True)
privateFile = open('private.json'); token = json.loads(privateFile.read())

#|----------Adding Cogs----------|

for cog in cogs:
    if cogs[cog] == True:
        client.add_cog(cog(client))

#|----------Reset DB every 5 minutes----------|

async def refreshDB():
    await client.wait_until_ready()
    sql = await asyncpg.connect(token['Database']['URL']+token['Database']['DNS'])
    while not client.is_closed():
        await asyncio.sleep(300)
        for DB in DBs:
            if DBs[DB] == True:
                await DB(sql)

#|----------Print when bot is online----------|

@client.event
async def on_ready():
    print(f"| -- {client.user.name}#{client.user.discriminator} is now online.")
    await client.change_presence(status=nextcord.Status.online, activity = nextcord.Activity(name=f"Prefix is {client.comnand_prefix}", type=1, url="https://www.twitch.tv/aoi_asmr")) #The twitch was to get the purple status, but I made it ASMR for fun

    sql = await asyncpg.connect(token['Database']['URL']+token['Database']['DNS'])
    for DB in DBs:
        if DBs[DB] == True:
            await DB(sql)

if __name__ == "__main__":
    client.loop.create_task(refreshDB())
    client.loop.create_task(RunTimes(client))
    client.run(token['Miumi']['Miumi'])