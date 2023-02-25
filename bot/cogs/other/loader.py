from discord.ext.commands import Cog, Bot, ExtensionError, Context, hybrid_command
from discord_ui import SlashOption

from bot.misc.config import Config

import os


def _manage_cogs(path: str, ext: str, method) -> list[tuple, str]:
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
    else:
        if not ext:
            iter_files(path)
        else:
            extensions.append(f'bot.cogs.{path}.{ext}')

    # Action with cogs themselves
    for cog in extensions:
        try:
            method(cog)
        except ExtensionError as error:
            log.append(error.args)
        else:
            log.append(cog)

    return log


class __LoaderOtherCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name='reload')
    async def _reload(
            self, ctx: Context,
            group: str = SlashOption(name='group', choices=['admin', 'user', 'other', 'all']),
            cogs: str = '') -> None:
        """Using for reload the bot cogs. Cogs are separated by space."""

        # Check on author is me
        if ctx.message.user.id != Config.ID_ME:
            await ctx.reply('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.defer(ephemeral=True)

        # Logging and Reloading Extension
        log = _manage_cogs(group, cogs, self.bot.reload_extension)
        msg, success, failed = 'Cogs reboot results:', 0, 0
        for data in log:
            if isinstance(data, str):
                msg += f'\n• Cog `{data}` has been successfully reload'
                success += 1
            elif isinstance(data, tuple):
                msg += '\n• {}'.format(data[0].replace("'", '`'))
                failed += 1
        msg += f'\n`Success: {success}` | `Failed: {failed}`'

        # Outputs a result by reload
        await ctx.send(msg)

    @hybrid_command(name='load')
    async def _load(
            self, ctx: Context,
            group: str = SlashOption(name='group', choices=['admin', 'user', 'other', 'all']),
            cogs: str = '') -> None:
        """Using for load the bot cogs. Cogs are separated by space."""

        # Check on author is me
        if ctx.user.id != Config.ID_ME:
            await ctx.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.response.defer(ephemeral=True, with_message=True)

        # Logging and Loading Extension
        log = _manage_cogs(group, cogs, self.bot.load_extension)
        msg, success, failed = 'Cogs reboot results:', 0, 0
        for data in log:
            if isinstance(data, str):
                msg += f'\n• Cog `{data}` has been successfully load'
                success += 1
            elif isinstance(data, tuple):
                msg += '\n• {}'.format(data[0].replace("'", '`'))
                failed += 1
        msg += f'\n`Success: {success}` | `Failed: {failed}`'

        # Outputs a result by load
        await ctx.followup.send(msg)

    @hybrid_command(name='unload')
    async def _unload(
            self, ctx: Context,
            group: str = SlashOption(name='group', choices=['admin', 'user', 'other', 'all']),
            cogs: str = '') -> None:
        """Using for unload the bot cogs. Cogs are separated by space."""

        # Check on author is me
        if ctx.user.id != Config.ID_ME:
            await ctx.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.response.defer(ephemeral=True, with_message=True)

        # Logging and Unloading Extension
        log = _manage_cogs(group, cogs, self.bot.unload_extension)
        msg, success, failed = 'Cogs reboot results:', 0, 0
        for data in log:
            if isinstance(data, str):
                msg += f'\n• Cog `{data}` has been successfully unload'
                success += 1
            elif isinstance(data, tuple):
                msg += '\n• {}'.format(data[0].replace("'", '`'))
                failed += 1
        msg += f'\n`Success: {success}` | `Failed: {failed}`'

        # Outputs a result by unload
        await ctx.followup.send(msg)


def setup(bot: Bot) -> None:
    bot.add_cog(__LoaderOtherCog(bot))
