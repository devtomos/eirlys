import nextcord, json
from nextcord.ext import commands

privateFile = open('private.json'); col = json.loads(privateFile.read())
def returnTime(seconds, granularity=2):
    intervals = (
    ('weeks', 604800),
    ('days', 86400),
    ('hours', 3600),
    ('minutes', 60),
    ('seconds', 1),
    )

    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

#|----------Viewing Avatar----------|
class AvatarViewer(nextcord.ui.View):
    def __init__(self, avatar, guildAvatar):
        super().__init__()
        self.avatar = avatar
        self.guild = guildAvatar
        self.views = True

    #|----------Edit embed with avatar----------|
    @nextcord.ui.button(label="View Guild Avatar", style=nextcord.ButtonStyle.green)
    async def avatarButton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.views == True:
            embed = nextcord.Embed(colour=int(col['Miumi']['Colour'], 16) + 0x200)
            embed.set_image(url=self.guild)

            button.label = "View Original Avatar"
            await interaction.edit(embed=embed, view=self)
            self.views = False
        else:
            embed = nextcord.Embed(colour=int(col['Miumi']['Colour'], 16) + 0x200)
            embed.set_image(url=self.avatar)

            button.label = "View Guild Avatar"
            await interaction.edit(embed=embed, view=self)
            self.views = True

#|----------Help Command List----------|
class HelpViewer(nextcord.ui.Select):
    def __init__(self, dictt, cogs):
        self.cogNames = cogs
        self.dict = dictt
        super().__init__(placeholder="Select a category", min_values=1, max_values=1, options=self.cogNames)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] != None:
            commands = '\n'.join(self.dict[self.values[0]])
            embed = nextcord.Embed(description=f'`{self.values[0]} Commands     :`\n{commands}', colour=int(col['Miumi']['Colour'], 16) + 0x200)
            await interaction.edit(embed=embed)

class HelpView(nextcord.ui.View):
    def __init__(self, dictt, cogs):
        self.dict = dictt
        self.cogs = cogs
        super().__init__()
        self.add_item(HelpViewer(self.dict, self.cogs))