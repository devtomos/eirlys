import nextcord
from datetime import datetime
from nextcord import Interaction
from nextcord.ext import commands
from src.api.anilist.search import search, relations
from src.api.anilist.user import user_search
from src.api.general.wide_functions import *
from src.api.general.wide_components import AnilistComponentViewer


class TextAnilist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["statistics"])
    async def stats(self, ctx):
        """
            View the statistics of the bot.
        """
        shards = []
        for i in range(0, 3):
            shards.append(f"`Shard {i}     :` {round(self.client.get_shard(i).latency * 1000)}ms")

        embed = nextcord.Embed(
            description=f"`Discord Latency     :` {round(self.client.latency * 1000)}ms\n\n" + '\n'.join(shards),
            colour=int(os.getenv("COL"), 16))
        await ctx.send(embed=embed)

    @commands.command(aliases=['anisetup', 'aniset', 'anilist-setup', 'ani-setup'])
    async def setup(self, ctx, *username):
        """
            Sets up the user within the database, or update their existing data.
            :params username: The username of the user on Anilist
        """
        sql = await db_connect()

        user_db = await sql.fetchval("SELECT discord_id FROM anilist WHERE discord_id = $1", ctx.author.id)
        ani = await user_search(''.join(username))
        embed = nextcord.Embed(title=ani['name'], url=ani['url'],
                               description=f"{ani['name']} has now been set within the database 🎊",
                               colour=int(os.getenv("COL"), 16))
        embed.set_image(url=ani['avatar'])

        if user_db is None:
            await sql.execute(
                "INSERT INTO anilist(discord_id, discord_name, anilist_name, anilist_id, anilist_url) VALUES ($1, $2, $3, $4, $5)",
                ctx.author.id, ctx.author.name, ani['name'], ani['id'], ani['url'])
        else:
            await sql.execute(
                "UPDATE anilist SET discord_name = $1, anilist_name = $2, anilist_id = $3, anilist_url = $4 WHERE discord_id = $5",
                ctx.author.name, ani['name'], ani['id'], ani['url'], ctx.author.id)
        logging.info(f"{ctx.author.name} is now set within the database")
        await ctx.send(embed=embed)

    @commands.command()
    async def anime(self, interaction: Interaction, *search_name):
        """
            Searches for an anime within the anilist API, and returns the information.
            :param interaction: The interaction of the command.
            :param search_name: The name of the anime to search for.
        """
        members, db_members = [], []
        sql = await db_connect()

        db = await sql.fetch("SELECT anilist_name, discord_id FROM anilist")

        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                db_members.append(db[key]['anilist_name'])

        ani_relations = await relations(" ".join(search_name), "ANIME")

        await interaction.send(view=AnilistComponentViewer(ani_relations[0], ani_relations[1], db_members, "ANIME"))

    @commands.command()
    async def manga(self, interaction: Interaction, *search_name):
        """
            Searches for a manga within the anilist API, and returns the information.
            :param interaction: The interaction of the command.
            :param search_name: The name of the anime to search for.
        """
        members, db_members = [], []
        sql = await db_connect()

        db = await sql.fetch("SELECT anilist_name, discord_id FROM anilist")

        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                db_members.append(db[key]['anilist_name'])

        ani_relations = await relations(" ".join(search_name), "MANGA")

        await interaction.send(view=AnilistComponentViewer(ani_relations[0], ani_relations[1], db_members, "MANGA"))

    @commands.command()
    async def user(self, ctx, *username):
        """
            Returns given or user within the database anilist information.
            :param username: The username of the user on Anilist
            :param ctx: The context of the command.
        """
        sql = await db_connect()
        db = await sql.fetch("SELECT anilist_name FROM anilist WHERE discord_id = $1", ctx.author.id)
        username = ''.join(username)

        if username == "":
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
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TextAnilist(client))
