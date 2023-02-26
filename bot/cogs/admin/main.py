from discord.ext.commands import Cog, Bot


# todo: AdminCogs
class __MainAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(__MainAdminCog(bot))
