from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop
from discord import Game

from time import time


# todo: OtherCogs
class __InfoOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.start_time = time()

    @Cog.listener()
    async def on_ready(self) -> None:
        self.status_is_online.start()

    def display_time(self) -> str:
        """Calculate time"""
        intervals = (
            ('w', 604800),  # 60 * 60 * 24 * 7
            ('d', 86400),  # 60 * 60 * 24
            ('h', 3600),  # 60 * 60
            ('m', 60),
            ('s', 1),
        )

        seconds, result = (time() - self.start_time), []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                result.append("{}{}".format(int(value), name))
        return ' '.join(result)

    @loop(seconds=10)
    async def status_is_online(self) -> None:
        """Show which time left that bot started"""
        await self.bot.change_presence(activity=Game(name='Online is {}'.format(self.display_time())))


def setup(bot: Bot) -> None:
    bot.add_cog(__InfoOtherCog(bot))
