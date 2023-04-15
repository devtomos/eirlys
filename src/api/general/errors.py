from nextcord.ext import commands
from nextcord import Embed, Colour


class StatusCodeError(Exception):
    """
    Exception raised if status code does not return 200

    Attributes:
        status_code -- Status code received
        function -- function used
        message -- Explanation of the error received
    """

    def __init__(self, status_code, function):
        self.status = status_code
        self.function = function
        self.message = f'''"{self.status}" status code was received while using "{self.function}" function'''
        super().__init__(self.message)


class NextCordErrorHandler(commands.Cog):
    """
        Exception raised if any error is caught while the bot is active.

        Attributes:
            client -- Discord Client
        """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            embed = Embed(title="Error Occurred! :x:", description=f"```py\n{error}\n```", colour=Colour.red())
            await ctx.send(embed=embed)


class NoDataBaseError(Exception):
    """
    Exception raised if no database is found

    Attributes:
        message -- Explanation of the error received
    """

    def __init__(self, message):
        self.message = "No database found. Set the Database URL in the .env file."
        super().__init__(self.message)


class NonSpecifiedError(Exception):
    """
    Exception raised invalid or no argument is specified.

    Attributes:
        message -- Explanation of the error received
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
