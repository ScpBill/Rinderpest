from discord.ext.commands import Bot, Cog


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print('[*] Bot is started! [*]')


def setup(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
