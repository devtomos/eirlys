import nextcord
from nextcord.ext import commands
from classes.anilistClasses import *

async def AnilistDB(conn1, conn2):
    global sql, cursor
    cursor = conn1
    sql = conn2
    return
 
class Anilist(commands.Cog):
    def __init__(self, client):
        self.client = client

    #|----------Connect Anilist----------|
    @commands.command(aliases=['anisetup', 'setani', 'setanilist'])
    async def aniset(self, ctx, username):
        cursor.execute("SELECT * FROM anilist WHERE discord_id = '%s'", (ctx.author.id,))
        user = cursor.fetchone()
        anilist = await Functions.User(username)

        if anilist[0]['errorCode'] != 200:
            return await ctx.send("Seems like there was an error, did you type your anilist name correctly?")

        embed = nextcord.Embed(title=anilist[0]['name'], url=anilist[0]['url'], colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=anilist[0]['avatar'])

        if user is None:
            cursor.execute("INSERT INTO anilist(discord_id, discord_name, anilist_name, anilist_id, anilist_url) VALUES (%s, %s, %s, %s, %s)", (ctx.author.id, ctx.author.name, anilist[0]['name'], anilist[0]['id'], anilist[0]['url']))
        else:
            cursor.execute("UPDATE anilist SET discord_name = %s, anilist_name = %s, anilist_id = %s, anilist_url = %s WHERE discord_id = %s", (ctx.author.name, anilist[0]['name'], anilist[0]['id'], anilist[0]['url'], ctx.author.id))
        sql.commit()
        await ctx.send(embed=embed)

    #|----------View Anilist Profile----------|
    @commands.command()
    async def user(self, ctx, username = None):
        if username is None:
            cursor.execute("SELECT anilist_name FROM anilist WHERE discord_id = %s", (ctx.author.id,))
            username = cursor.fetchone()[0]
            if username is None:
                return await ctx.send("Looks like you're not in the database. Use .aniset <anilist_name> to set!")

        anilist = await Functions.User(username)

        if anilist[0]['errorCode'] != 200:
            return await ctx.send("An Error has occured. Did you input their name correctly?")

        embedDescription = [
            '[**_Anime Information_**]({}/animelist)\n'.format(anilist[0]['url']),
            '`Anime Count     :` **{:,}**\n'.format(anilist[1]['animeCount']),
            '`Anime Mean      :` **{}**\n'.format(anilist[1]['animeMean']),
            '`Eps Watched     :` **{:,}**\n'.format(anilist[1]['animeWatch']),
            '`Time Watched    :` **{}**\n\n'.format(returnTime(anilist[1]['animeTime'] * 60, 3)),

            '[**_Manga Information_**]({}/mangalist)\n'.format(anilist[0]['url']),
            '`Manga Count     :` **{:,}**\n'.format(anilist[1]['mangaCount']),
            '`Manga Mean      :` **{}**\n'.format(anilist[1]['mangaMean']),
            '`Chaps Read      :` **{:,}**\n'.format(anilist[1]['mangaChapt']),
            '`Volumes Read    :` **{:,}**\n'.format(anilist[1]['mangaVolume'])]

        embed = nextcord.Embed(title=anilist[0]['name'] + ' statistics', url=anilist[0]['url'], description=''.join(embedDescription), colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=anilist[0]['banner'])
        embed.set_thumbnail(url=anilist[0]['avatar'])
        await ctx.send(embed=embed)

    #|----------View Information For Anime----------|
    @commands.command()
    async def anime(self, interaction: nextcord.Interaction, *anime):
        anime = ' '.join(anime); members = []; dbMembs = []; cursor.execute("SELECT anilist_name, discord_id FROM anilist"); db = cursor.fetchall()
        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key][1] in members:
                dbMembs.append(db[key][0])
        relation = await Functions.Relations(anime, 'ANIME')

        if relation[1][0] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?")
        await interaction.send(view=Viewing(relation[1], relation[0], dbMembs, 'ANIME'))
    
    #|----------View Information For Manga----------|
    @commands.command()
    async def manga(self, interaction: nextcord.Interaction, *manga):
        manga = ' '.join(manga); members = []; dbMembs = []; cursor.execute("SELECT anilist_name, discord_id FROM anilist"); db = cursor.fetchall()
        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key][1] in members:
                dbMembs.append(db[key][0])
        relation = await Functions.Relations(manga, 'MANGA')

        if relation[1][0] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?")
        await interaction.send(view=Viewing(relation[1], relation[0], dbMembs, 'MANGA'))

    @commands.command()
    async def affinity(self, ctx):
        #Not Finished
        OGUser = None; members = []; dbMembs = []; db = await sql.fetch("SELECT anilist_id, discord_id FROM anilist")
        for member in ctx.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                if db[key]['discord_id'] == ctx.author.id:
                    OGUser = db[key]['anilist_id']
                dbMembs.append(db[key]['anilist_id'])

        for member in dbMembs:
            await Functions.Affinity(OGUser, member, dbMembs)