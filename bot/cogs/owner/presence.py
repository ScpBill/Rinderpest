from discord.ext.commands import Bot, Cog, Context
from discord.ext.tasks import loop
from discord.ext import commands
from discord import Activity, Game
from pypresence import AioPresence

from time import time


class Delay:
    def __init__(self, delay: float):
        self._delay = delay

    @property
    def days(self):
        _d = str(int(self._delay // 86400))
        return f'{_d} day{"" if _d.endswith("1") else "s"}'

    @property
    def hours(self):
        _h = str(int(self._delay // 3600 % 24))
        return f'{_h} hour{"" if _h.endswith("1") else "s"}'

    @property
    def minutes(self):
        _m = str(int(self._delay // 60 % 60))
        return f'{_m} minute{"" if _m.endswith("1") else "s"}'


class RichPresenceCog(Cog, name='Rich Presence', description='Manage bot\'s and owners rich presences'):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.start_time = time()
        self.information = self._generator_statuses()
        self.presence = AioPresence(client_id=self.bot.application_id, loop=self.bot.loop)

    @commands.hybrid_group(name='rp')
    async def _rich_presence(self, ctx: Context) -> None: pass

    @_rich_presence.command(name='update', description='Change my rich presence')
    @commands.is_owner()
    async def _change_presence(
            self, ctx: Context, state: str = None, details: str = None, start: int = None, end: int = None,
            large_image: str = None, large_text: str = None, small_image: str = None, small_text: str = None,
            party_id: str = None, party_size: str = None, join: str = None, spectate: str = None,
            match: str = None, buttons: str = None, instance: bool = True) -> None:

        await ctx.defer(ephemeral=True)
        await self.presence.clear()

        try:
            await self.presence.update(
                state=state, details=details, start=start, end=end, large_image=large_image, large_text=large_text,
                small_image=small_image, small_text=small_text, party_id=party_id,
                party_size=eval(party_size) if party_size is not None else None, join=join,
                spectate=spectate, match=match, buttons=eval(buttons) if buttons is not None else None, instance=instance
            )
        except Exception as exc:
            await ctx.reply(f'{type(exc).__name__}: {exc}', mention_author=False)
        else:
            await ctx.reply('Your status is successful changed!', mention_author=False)

    @_rich_presence.command(name='clear', description='Clear my rich presence')
    @commands.is_owner()
    async def _clear_presence(self, ctx: Context) -> None:
        await ctx.defer(ephemeral=True)
        await self.presence.clear()

    def _generator_statuses(self):
        while True:
            yield 'Passed: {} {} {}'.format(self.delay().days, self.delay().hours, self.delay().minutes)
            yield '/help | .help | @{} help'.format(self.bot.application.name)

    def delay(self) -> Delay:
        return Delay(time() - self.start_time)

    @Cog.listener()
    async def on_ready(self) -> None:
        await self.presence.connect()
        await self.bot.wait_until_ready()
        print('[+] Rich Presence Cog is started')

        self._update_status.stop()
        self._update_status.start()

    @loop(seconds=10)
    async def _update_status(self) -> None:
        await self.bot.change_presence(activity=Game(
            name=next(self.information)
        ))


async def setup(bot: Bot) -> None:
    await bot.add_cog(RichPresenceCog(bot))
