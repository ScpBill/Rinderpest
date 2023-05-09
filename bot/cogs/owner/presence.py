from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop
from discord import Activity

from time import time


class Delay:
    def __init__(self, delay: float):
        self._delay = delay

    @property
    def days(self):
        _d = str(self._delay // 86400)
        return f'{_d} day{"" if _d.endswith("1") else "s"}'

    @property
    def hours(self):
        _h = str(self._delay // 3600 % 24)
        return f'{_h} day{"" if _h.endswith("1") else "s"}'

    @property
    def minutes(self):
        _m = str(self._delay // 60 % 60)
        return f'{_m} day{"" if _m.endswith("1") else "s"}'


class RichPresenceCog(Cog, name='Rich Presence', description='Manage bot\'s and owners rich presences'):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.start_time = time()

    @property
    def delay(self) -> Delay:
        return Delay(time() - self.start_time)

    @Cog.listener()
    async def on_ready(self) -> None:
        self.update_status.stop()
        self.update_status.start()

    @loop(seconds=10)
    async def update_status(self) -> None:
        def info():
            while True:
                yield 'Passed: {} {} {}'.format(self.delay.days, self.delay.hours, self.delay.minutes)
                yield '@{} help | /help | .help'.format(self.bot.application.name)

        information = info()

        await self.bot.change_presence(activity=Activity(
            name=next(information), state='Bot is '
        ))


async def setup(bot: Bot) -> None:
    await bot.add_cog(RichPresenceCog(bot))
