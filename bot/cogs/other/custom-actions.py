from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop
from discord import Game

from time import time


class CustomizeCog(Cog, name='Information', description=''):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.start_time = time()

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

    @Cog.listener()
    async def on_ready(self) -> None:
        """START THE BOT"""

        # Print message about the start into server console
        print('[*] Bot is started! [*]')

        # Play status in bot profile
        self.update_status.start()

    @loop(seconds=10)
    async def update_status(self) -> None:
        """Show which time left that bot started"""
        await self.bot.change_presence(activity=Game(name='Online is {}'.format(self.display_time())))


async def setup(bot: Bot) -> None:
    await bot.add_cog(CustomizeCog(bot))
