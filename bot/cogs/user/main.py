from discord.ext.commands import Cog, Bot, Context, hybrid_command


# todo: UserCogs
class __MainUserCog(Cog, name='General', description='Basic user commands'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command()
    async def ping(self, ctx: Context) -> None:
        """Simple command that responds with Pong!"""
        await ctx.send('Pong!')


async def setup(bot: Bot) -> None:
    await bot.add_cog(__MainUserCog(bot))
