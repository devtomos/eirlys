import nextcord, pprint
from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption
from datetime import datetime
from classes.anilistClasses import *

async def SLAnilistDB(connect):
    global sql
    sql = connect
    return

class SLAnilist(commands.Cog):
    def __init__(self, client):
        self.client = client

    #|----------Connect Anilist----------|
    @slash_command("aniset", "Set your anilist account to see your scores!")
    async def aniset(self, interaction: Interaction, anilist_name: str = SlashOption("anilist_username", "Your anilist username", required=True)):
        user = await sql.fetchval("SELECT anilist_name FROM anilist WHERE discord_id = $1", interaction.user.id)
        anilist = await Functions.User(anilist_name)

        if anilist[0]['errorCode'] != 200:
            return await interaction.send("Seems like there was an error, did you type your anilist name correctly?")

        embed = nextcord.Embed(title=anilist[0]['name'], url=anilist[0]['url'], colour=int(col['Miumi']['Colour'], 16) + 0x200)
        embed.set_image(url=anilist[0]['avatar'])

        if user is None:
            await sql.execute("INSERT INTO anilist(discord_id, discord_name, anilist_name, anilistid, anilisturl) VALUES ($1, $2, $3, $4, $5)", interaction.user.id, interaction.user.name, anilist[0]['name'], anilist[0]['id'], anilist[0]['url'])
        else:
            await sql.execute("UPDATE anilist SET discord_name = $1, anilist_name = $2, anilistid = $3, anilisturl = $4 WHERE discord_id = $5", interaction.user.name, anilist[0]['name'], anilist[0]['id'], anilist[0]['url'], interaction.user.id)
        await interaction.send(embed=embed)

    #|----------View Anilist Profile----------|
    @slash_command("user", "View Information about yourself or someone from the Anilist API")
    async def user(self, interaction: Interaction, anilist_name: str = SlashOption("anilist_username", "An Anilist username", required=False)):
        if anilist_name is None:
            anilist_name = await sql.fetchval("SELECT anilist_name FROM anilist WHERE discord_id = $1", interaction.user.id)
            if anilist_name is None:
                return await interaction.send("Looks like you're not in the database. Use /aniset <anilist_name> to set!")

        anilist = await Functions.User(anilist_name)

        if anilist[0]['errorCode'] != 200:
            return await interaction.send("An Error has occured. Did you input their name correctly?")

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
        await interaction.send(embed=embed)

    #|----------View Information For Anime----------|
    @slash_command("anime", "View Information about an Anime")
    async def anime(self, interaction: Interaction, anime_name: str = SlashOption("anime_name", "Input an Anime name, then choose from a selection", required=True)):
        members = []; dbMembs = []; db = await sql.fetch("SELECT anilist_name, discord_id FROM anilist")
        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                dbMembs.append(db[key]['anilist_name'])
        relation = await Functions.Relations(anime_name, 'ANIME')

        if relation[1][0] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?")
        await interaction.send(view=Viewing(relation[1], relation[0], dbMembs, 'ANIME'))

    #|----------View Information For Manga----------|
    @slash_command("manga", "View Information about a Manga")
    async def manga(self, interaction: Interaction, manga_name: str = SlashOption("manga_name", "Input an Manga name, then choose from a selection", required=True)):
        members = []; dbMembs = []; db = await sql.fetch("SELECT anilist_name, discord_id FROM anilist")
        for member in interaction.guild.members:
            members.append(member.id)

        for key, value in enumerate(db):
            if db[key]['discord_id'] in members:
                dbMembs.append(db[key]['anilist_name'])
        relation = await Functions.Relations(manga_name, 'MANGA')

        if relation[1][0] == 404:
            return await interaction.send("Error Occured. Did you type the name correctly?")
        await interaction.send(view=Viewing(relation[1], relation[0], dbMembs, 'MANGA'))