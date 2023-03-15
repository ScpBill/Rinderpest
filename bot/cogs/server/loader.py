from discord.ext.commands import Cog, Bot, Context, MissingRequiredArgument
from discord.ext import commands

from bot.misc.config import Config
from bot.misc.ext import use_cogs


class LoaderCog(Cog, name='Cogs manager', description='Managing extensions and loading cogs into them'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name='cogs', hidden=True)
    async def _cogs(self, ctx: Context) -> None:
        """Manage cogs"""
        pass

    @_cogs.command(name='reload', hidden=True)
    async def _reload(self, ctx: Context,
                      group: str = commands.parameter(description='Cogs folder'),
                      cogs: str = commands.parameter(description='Cogs names', default='')) -> None:
        """Using for reload the bot cogs. Cogs are separated by space."""

        # Check on author is me
        if ctx.message.author.id != Config.ID_ME:
            return

        # Logging and Reloading Extension
        log = await use_cogs(self.bot, group, cogs, 'reload')
        msg, success, failed = '**Result of the command execution:**', 0, 0
        for data in log:
            if isinstance(data, str):
                msg += f'\n• Cog `{data}` has been successfully reload'
                success += 1
            elif isinstance(data, tuple):
                msg += '\n• {}'.format(data[0].replace("'", '`'))
                failed += 1
        msg += f'\n`Success: {success}` | `Failed: {failed}`'

        # Outputs a result by reload
        await ctx.reply(msg)

    @_cogs.command(name='load', hidden=True)
    async def _load(self, ctx: Context,
                    group: str = commands.parameter(description='Cogs folder'),
                    cogs: str = commands.parameter(description='Cogs names', default='')) -> None:
        """Using for load the bot cogs. Cogs are separated by space."""

        # Check on author is me
        if ctx.message.author.id != Config.ID_ME:
            return

        # Logging and Loading Extension
        log = await use_cogs(self.bot, group, cogs, 'load')
        msg, success, failed = '**Result of the command execution:**', 0, 0
        for data in log:
            if isinstance(data, str):
                msg += f'\n• Cog `{data}` has been successfully load'
                success += 1
            elif isinstance(data, tuple):
                msg += '\n• {}'.format(data[0].replace("'", '`'))
                failed += 1
        msg += f'\n`Success: {success}` | `Failed: {failed}`'

        # Outputs a result by load
        await ctx.reply(msg)

    @_cogs.command(name='unload', hidden=True)
    async def _unload(self, ctx: Context,
                      group: str = commands.parameter(description='Cogs folder'),
                      cogs: str = commands.parameter(description='Cogs names', default='')) -> None:
        """Using for unload the bot cogs. Cogs are separated by space."""

        # Check on author is me
        if ctx.message.author.id != Config.ID_ME:
            return

        # Logging and Unloading Extension
        log = await use_cogs(self.bot, group, cogs, 'unload')
        msg, success, failed = '**Result of the command execution:**', 0, 0
        for data in log:
            if isinstance(data, str):
                msg += f'\n• Cog `{data}` has been successfully unload'
                success += 1
            elif isinstance(data, tuple):
                msg += '\n• {}'.format(data[0].replace("'", '`'))
                failed += 1
        msg += f'\n`Success: {success}` | `Failed: {failed}`'

        # Outputs a result by unload
        await ctx.reply(msg)

    @_reload.error
    @_load.error
    @_unload.error
    async def _extensions_error(self, ctx: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send_help(ctx.command)


async def setup(bot: Bot) -> None:
    await bot.add_cog(LoaderCog(bot))
