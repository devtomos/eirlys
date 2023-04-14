import nextcord
import os
import logging
import sys
from dotenv import load_dotenv
from nextcord.ext import commands

# [+] Load Cogs From Files [+]#
from src.cogs.slash.slashAni import SlashAni
from src.cogs.slash.slashGeneral import SlashGeneral, sql_func
from src.cogs.text.textGeneral import TextGeneral

# [+] Load .ENV File [+]#
load_dotenv()

# [+] Setup Logging for Nextcord [+]#
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s:%(levelname)s:%(name)s]: %(message)s'))
logger.addHandler(handler)


# [+] Create Client Instance [+]#
client = commands.AutoShardedBot(shard_count=3, command_prefix=".", help_command=None, intents=nextcord.Intents.all(), case_insensitive=True)

# ___________________________________________________________________________________________________________________#

# [+] Add Slash Cogs [+]#
client.add_cog(SlashGeneral(client))
client.add_cog(SlashAni(client))
client.add_cog(TextGeneral(client))


# ___________________________________________________________________________________________________________________#

# [+] Send Message When Bot Is Online [+]#
@client.event
async def on_ready():
    logger.info(f'{client.user.name} Is Online')
    await client.change_presence(status=nextcord.Status.online,
                                 activity=nextcord.Activity(name=f"Slash Commands", type=3))
    await sql_func()


# ___________________________________________________________________________________________________________________#

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))
