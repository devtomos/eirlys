import nextcord, os, asyncpg
from src.classes.defaultFuncs import *

#[+] Guild Avatar Viewing [+]#
class AvatarViewer(nextcord.ui.View):
    def __init__(self, avatar, guildAvatar):
        super().__init__()
        self.avatar = avatar
        self.guild = guildAvatar
        self.views = True

    #[+] Add Button To Check Guild And Global [+]#
    @nextcord.ui.button(label="View Guild Avatar", style=nextcord.ButtonStyle.green)
    async def avatarButton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.views == True:
            embed = nextcord.Embed(colour=int(os.getenv("COL"), 16))
            embed.set_image(url=self.guild)

            button.label = "View Original Avatar"
            await interaction.edit(embed=embed, view=self)
            self.views = False
        else:
            embed = nextcord.Embed(colour=int(os.getenv("COL"), 16))
            embed.set_image(url=self.avatar)

            button.label = "View Guild Avatar"
            await interaction.edit(embed=embed, view=self)
            self.views = True