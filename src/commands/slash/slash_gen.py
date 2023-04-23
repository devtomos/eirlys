import nextcord
from datetime import datetime
from nextcord import Interaction, slash_command, SlashOption, application_command
from nextcord.ext import commands
from src.api.anilist.search import search, relations
from src.api.anilist.user import user_search
from src.api.general.wide_functions import *
from src.api.general.wide_components import AnilistComponentViewer

games = ['CSS', 'Quake', 'Overwatch', 'Valorant', 'Apex Legends', 'Fortnite', 'CSGO', 'COD MW2 (2022)', 'Rainbow Six', 'Rust', 'Destiny 2', 'cm/360', 'in/360']

class SlashGeneral(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="sensitivity")
    async def sens(self):
        pass

    @sens.subcommand(name="converter", description="Convert your sensitivity from one game to another.")
    async def slash_conv(self, interaction: Interaction, 
    game_one: str = SlashOption("from", description="The game you want to convert from", required=True, autocomplete=True),
    game_two: str = SlashOption("to", description="The game you want to convert to", required=True, autocomplete=True),
    sens: str = SlashOption("sensitivity", description="Your sensiviity for the game", required=True),
    dpi: str = SlashOption("dpi", description="Your DPI for your mouse", required=True)):

        one = float(sens_games[game_one])
        two = float(sens_games[game_two])
        dpi = float(dpi)
        sens = float(sens)

        convert_sens = (((one * dpi) * sens) / (two * dpi))
        convert_in360 = ((360 / (one * dpi * 1 * sens)))
        convert_cm360 = ((360 / (one * dpi * 1 * sens)) * 2.54)

        await interaction.send(f"{game_two}: `{round(convert_sens, 3)}`\n`{round(convert_cm360, 2)}cm/360` | `{round(convert_in360, 2)}in/360`")


    @slash_conv.on_autocomplete('game_one')
    async def convert_autocomplete(self, interaction: Interaction, current: str) -> List:
        if not current:
            await interaction.response.send_autocomplete(games)
            return
        get_game = [game for game in games if game.lower().startswith(game.lower())]
        await interaction.response.send_autocomplete(get_game)

    @slash_conv.on_autocomplete('game_two')
    async def convert_autocomplete(self, interaction: Interaction, current: str) -> List:
        if not current:
            await interaction.response.send_autocomplete(games)
            return
        get_game = [game for game in games if game.lower().startswith(game.lower())]
        await interaction.response.send_autocomplete(get_game)
