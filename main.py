import nextcord, os, asyncpg, random
from nextcord.ext import commands
from dotenv import load_dotenv

#[+] Load Cogs From Files [+]#
from src.cogs.slash.slashGeneral import SlashGeneral, sqlFunc
from src.cogs.slash.slashAni import SlashAni

#[+] Load .ENV File [+]#
load_dotenv()

#[+] Create Client Instance [+]#
client = commands.Bot(help_command=None, intents=nextcord.Intents.all(), case_insensitive=True)

# _________________________________________________________________________________________________________________________________________________________________ #

#[+] Add Slash Cogs [+]#
client.add_cog(SlashGeneral(client))
client.add_cog(SlashAni(client))

# _________________________________________________________________________________________________________________________________________________________________ #

#[+] Send Message When Bot Is Online [+]#
@client.event
async def on_ready():
    print(f"[+] {client.user.name} Is Online")
    await client.change_presence(status=nextcord.Status.online, activity = nextcord.Activity(name=f"Slash Commands", type=3))
    await sqlFunc()

# _________________________________________________________________________________________________________________________________________________________________ #

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))