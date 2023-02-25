from discord.ext.commands import Cog, Bot, Context, hybrid_command
from discord import Interaction


# todo: UserCogs
class __MainUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command()
    async def ping(self, interaction: Interaction) -> None:
        """Simple command that responds with Pong!"""
        await interaction.response.send_message('Pong!')


async def setup(bot: Bot) -> None:
    await bot.add_cog(__MainUserCog(bot))
