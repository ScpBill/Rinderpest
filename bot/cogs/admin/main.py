from nextcord.ext.commands import Cog, Bot, command


# todo: AdminCogs
class __MainAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot


def setup(bot: Bot) -> None:
    bot.add_cog(__MainAdminCog(bot))
