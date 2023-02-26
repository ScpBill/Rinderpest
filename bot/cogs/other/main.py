from discord.ext.commands import Bot, Cog


# todo: OtherCogs
class __MainOtherCog(Cog, name='Main', description=''):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print('[*] Bot is started! [*]')


async def setup(bot: Bot) -> None:
    await bot.add_cog(__MainOtherCog(bot))
