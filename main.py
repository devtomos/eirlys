import nextcord, json, asyncpg, asyncio
from nextcord.ext import commands

#|----------Normal Commands----------|
from cogs.normalCommands.general import General, GeneralDB, RunTimes
from cogs.normalCommands.anilist import Anilist, AnilistDB
from cogs.slashCommands.SLAnilist import SLAnilist, SLAnilistDB
from cogs.slashCommands.SLGeneral import SLGeneral, SLGeneralDB

#|----------Cog and DB Dicts----------|
cogs = {General: True, Anilist: True, SLAnilist: True, SLGeneral: True}
DBs = {GeneralDB: True, AnilistDB: True, SLAnilistDB: True, SLGeneralDB: True}

#|----------Setting Client and Token----------|
client = commands.Bot(command_prefix=".", help_command=None, intents=nextcord.Intents.all(), case_insensitive=True)
privateFile = open('private.json'); token = json.loads(privateFile.read())

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
    print(f"| -- {client.user.name}#{client.user.discriminator} -- ONLINE")
    await client.change_presence(status=nextcord.Status.online, activity = nextcord.Activity(name=f"Prefix is {client.command_prefix}", type=1, url="https://www.twitch.tv/aoi_asmr"))

    #|----------Adding Cogs----------|
    for cog in cogs:
        if cogs[cog] == True:
            print(f"| -- {cog.__name__} -- ONLINE")
            client.add_cog(cog(client))

    #|----------Adding Databases----------|
    sql = await asyncpg.connect(token['Database']['URL']+token['Database']['DNS'])
    for DB in DBs:
        if DBs[DB] == True:
            print(f"| -- {DB.__name__} -- ONLINE")
            await DB(sql)

if __name__ == "__main__":
    client.loop.create_task(refreshDB())
    client.loop.create_task(RunTimes(client))
    client.run(token['Miumi']['Miumi'])