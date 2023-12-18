import nextcord
from datetime import datetime
from nextcord import Interaction, slash_command, SlashOption
from nextcord.ext import commands
from src.api.anilist.search import search, relations
from src.api.anilist.user import user_search
from src.api.general.wide_functions import *
from src.api.general.wide_components import AnilistComponentViewer


class SlashAnilist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="stats", description="Returns some statistics for the bot")
    async def sslash_stats(self, interaction: Interaction):
        shards = []
        for i in range(0, 3):
            shards.append(f"`Shard {i}     :` {round(self.client.get_shard(i).latency * 1000)}ms")

        embed = nextcord.Embed(
            description=f"`Discord Latency     :` {round(self.client.latency * 1000)}ms\n\n" + '\n'.join(shards),
            colour=int(os.getenv("COL"), 16))
        await interaction.send(embed=embed)

    @slash_command(name="setup", description="Sets up the user within the database, or update their existing data.")
    async def sslash_setup(self, interaction: Interaction, username: str = SlashOption(name="username",
                                                                                       description="The username of the user on Anilist", required=True)):
        """
            Sets up the user within the database, or update their existing data.
            :params username: The username of the user on Anilist
        """
        sql = await db_connect()

        user_db = await sql.fetchval("SELECT discord_id FROM anilist WHERE discord_id = $1", interaction.user.id)
        ani = await user_search(username)
        embed = nextcord.Embed(title=ani['name'], url=ani['url'],
                               description=f"{ani['name']} has now been set within the database 🎊",
                               colour=int(os.getenv("COL"), 16))
        embed.set_image(url=ani['avatar'])

        if user_db is None:
            await sql.execute(
                "INSERT INTO anilist(discord_id, discord_name, anilist_name, anilist_id, anilist_url) VALUES ($1, $2, $3, $4, $5)",
                interaction.user.id, interaction.user.name, ani['name'], ani['id'], ani['url'])
        else:
            await sql.execute(
                "UPDATE anilist SET discord_name = $1, anilist_name = $2, anilist_id = $3, anilist_url = $4 WHERE discord_id = $5",
                interaction.user.name, ani['name'], ani['id'], ani['url'], interaction.user.id)
        logging.info(f"{interaction.user.name} is now set within the database")
        await interaction.send(embed=embed)

    @slash_command(name="anime", description="Search for an anime within the anilist API, and returns the information.")
    async def sslash_anime(self, interaction: Interaction, media_name: str = SlashOption(name="media_name",
                                                                                         description="The name of the anime to search for.")):
        """
                    Searches for an anime within the anilist API, and returns the information.
                    :param interaction: The interaction of the command.
                    :param media_name: The name of the anime to search for.
                """
        members, db_members = [], []
        sql = await db_connect()

        db = await sql.fetch("SELECT anilist_name, discord_id FROM anilist")

        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                db_members.append(db[key]['anilist_name'])

        ani_relations = await relations(media_name, "ANIME")
        await interaction.send(view=AnilistComponentViewer(ani_relations[0], ani_relations[1], db_members, "ANIME"))

    @slash_command(name="manga", description="Search for an manga within the anilist API, and returns the information.")
    async def sslash_manga(self, interaction: Interaction, media_name: str = SlashOption(name="media_name",
                                                                                         description="The name of the manga to search for.")):
        """
                    Searches for an anime within the anilist API, and returns the information.
                    :param interaction: The interaction of the command.
                    :param media_name: The name of the manga to search for.
                """
        members, db_members = [], []
        sql = await db_connect()

        db = await sql.fetch("SELECT anilist_name, discord_id FROM anilist")

        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                db_members.append(db[key]['anilist_name'])

        ani_relations = await relations(media_name, "MANGA")
        await interaction.send(view=AnilistComponentViewer(ani_relations[0], ani_relations[1], db_members, "MANGA"))

    @slash_command(name="user", description="Search for an user within the anilist API, and returns the information.")
    async def sslash_user(self, interaction: Interaction, username: str = SlashOption(name="username",
                                                                                      description="The username of the user to search for.", required=False)):
        """
            Returns given or user within the database anilist information.
            :param username: The username of the user on Anilist
        """
        sql = await db_connect()
        db = await sql.fetch("SELECT anilist_name FROM anilist WHERE discord_id = $1", interaction.user.id)

        if not username:
            if not db:
                raise NonSpecifiedError(
                    '"You have not set your anilist name yet, nor specified a user."')
            else:
                username = db[0]['anilist_name']

        ani = await user_search(username)
        user_list = [
            f"[**__Anime Information__**]({ani['url']}/animelist)",
            f"`Anime Count    :` {ani['animeCount']}",
            f"`Mean Score     :` {ani['animeMean']}",
            f"`Watch Time     :` {rtime(ani['animeTime'])}",
            f"`Watched Eps    :` {ani['animeWatch']}\n",

            f"[**__Manga Information__**]({ani['url']}/mangalist)",
            f"`Manga Count    :` {ani['mangaCount']}",
            f"`Mean Score     :` {ani['mangaMean']}",
            f"`Volumes Read   :` {ani['mangaVolume']}",
            f"`Chapters Read  :` {ani['mangaChapter']}"]

        embed = nextcord.Embed(title=ani['name'], url=ani['url'], description='\n'.join(user_list), color=int(os.getenv("COL"), 16))
        embed.set_thumbnail(url=ani['avatar'])
        embed.set_image(url=ani['banner'])
        embed.set_footer(text=f"{ani['id']} | "
                              f"{datetime.utcfromtimestamp(ani['updated']).strftime('%d/%m/%Y %H:%M:%S')}")
        await interaction.send(embed=embed)
