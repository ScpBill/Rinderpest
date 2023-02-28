from discord.ext.commands import Cog, Bot, ExtensionError, Context, MissingRequiredArgument
from discord.ext import commands

from bot.misc.config import Config

import os


async def _manage_cogs(path: str, ext: str, method) -> list[tuple, str]:
    """Manage cogs"""
    extensions, log = [], []

    # Function writing extensions
    def iter_files(directory: str):
        files: list = os.listdir(os.path.join('bot/cogs/', directory))
        files.remove('__init__.py')
        extensions.extend(
            [f'bot.cogs.{directory}.' + os.path.splitext(file)[0] for file in files if file.endswith('.py')])

    # Action according to the data
    if path == 'all':
        for path in ('admin', 'user', 'other'):
            iter_files(path)
    elif path in ('admin', 'user', 'other'):
        if not ext:
            iter_files(path)
        else:
            extensions.append(f'bot.cogs.{path}.{ext}')
    else:
        raise MissingRequiredArgument

    # Action with cogs themselves
    for cog in extensions:
        try:
            await method(cog)
        except ExtensionError as error:
            log.append(error.args)
        else:
            log.append(cog)

    return log


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
            await ctx.reply('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.defer(ephemeral=True)

        # Logging and Reloading Extension
        log = await _manage_cogs(group, cogs, self.bot.reload_extension)
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
            await ctx.reply('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.defer(ephemeral=True)

        # Logging and Loading Extension
        log = await _manage_cogs(group, cogs, self.bot.load_extension)
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
            await ctx.reply('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.defer(ephemeral=True)

        # Logging and Unloading Extension
        log = await _manage_cogs(group, cogs, self.bot.unload_extension)
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
