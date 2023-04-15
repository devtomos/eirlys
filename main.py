import nextcord
import os
import asyncio
from dotenv import load_dotenv
from nextcord import Forbidden
from nextcord.ext import commands

from src.api.anilist.search import search
from src.api.general.wide_functions import logger, db_connect
from src.api.general.errors import NextCordErrorHandler
from src.commands.slash.slash_anilist import SlashAnilist

"""
TODO:
    1) First set up the APIs required - Affinity is left
    2) Set up logging for the terminal - Add more to api and affinity
    3) Connect to Database and set it up with the APIs - DONE
    4) Cache User content and such for the API (saves reruns) - LAST THING
"""

# Loading the .env file into Python.
load_dotenv()

# Create Client and add Shards
client = commands.AutoShardedBot(shard_count=int(os.getenv('SHARD_COUNT')), command_prefix=".", help_command=None,
                                 intents=nextcord.Intents.all(),
                                 case_insensitive=True)

client.add_cog(NextCordErrorHandler(client))
client.add_cog(SlashAnilist(client))

# Initialize text cogs
for filename in os.listdir('./src/commands/text'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'src.commands.text.{filename[:-3]}')
            logger.info(f"{filename[:-3]} cog has been loaded")
        except Exception as e:
            logger.error(f"{filename[:-3]} cog failed to load")
            logger.error(e)


# ___________________________________________________________________________________________________________________#


# Send message once Eirlys is ready.
@client.event
async def on_ready():
    logger.info(f'{client.user.name} is online')
    await client.change_presence(status=nextcord.Status.online,
                                 activity=nextcord.Activity(name=f"Snowdrop", type=3))


# ___________________________________________________________________________________________________________________#

# Run Eirlys from this file only.
if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))
    asyncio.run(db_connect())
