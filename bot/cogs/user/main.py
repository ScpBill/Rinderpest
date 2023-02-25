from discord.ext.commands import Cog, Bot
from discord import Interaction


# todo: UserCogs
class __MainUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Bot.slash_command(Bot())
    async def ping(self, interaction: Interaction) -> None:
        """Simple command that responds with Pong!"""
        await interaction.response.send_message('Pong!')


def setup(bot: Bot) -> None:
    bot.add_cog(__MainUserCog(bot))
