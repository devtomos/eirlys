import nextcord
from src.api.general.wide_functions import *
from src.api.anilist.search import search
from src.api.general.wide_functions import logger
from nextcord import SelectOption


# Add a selection menu to anime and manga commands
class AnilistComponentViewer(nextcord.ui.View):
    def __init__(self, options, options_id, members, media_type):
        super().__init__()
        self.media_options = options
        self.option_ids = options_id
        self.members = members
        self.media_type = media_type

        logger.info("AnilistComponentViewer has been initialized")
        self.add_item(AnilistComponentSelect(self.media_options[:24], self.option_ids, self.members, self.media_type))


# Upon choosing title, display the information
class AnilistComponentSelect(nextcord.ui.Select):
    def __init__(self, options, options_id, members, media_type):
        self.media_options = options
        self.option_ids = options_id
        self.members = members
        self.media_type = media_type
        super().__init__(placeholder="Choose a title..", min_values=1, max_values=1, options=self.media_options)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if self.values[0] != '' or None:
            logger.info(f"{self.values[0]} has been chosen from the selection menu")

            ani = await search(self.option_ids[self.values[0]], self.media_type, self.members, True)
            embed = nextcord.Embed(title=ani[0]['name'], url=ani[0]['url'], description=''.join(ani[1]),
                                   colour=int(os.getenv("COL"), 16))
            embed.set_image(url=ani[0]['banner'])
            embed.set_thumbnail(url=ani[0]['avatar'])
            await interaction.edit(embed=embed)
            logger.info(f"{self.values[0]} has been displayed in the embed")
