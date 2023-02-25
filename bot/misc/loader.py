from discord.ext.commands import Bot, ExtensionError, MissingRequiredArgument

import os
from typing import Dict
import logging


async def load_cogs(bot: Bot) -> Dict[bool, str]:
    logging.getLogger('discord.py')
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s')
    log = []

    for _dir_name in os.listdir('bot/cogs/'):
        # Check only folders
        if not os.path.isdir(_cog_dir := os.path.join('bot/cogs/', _dir_name)):
            continue

        for _ext_name in os.listdir(_cog_dir):
            # Check only python files
            if not os.path.isfile(_ext_name) or not _ext_name.endswith('.py'):
                continue
            
            # And load our extensions
            path = f'bot.cogs.{_dir_name}.{_ext_name}'
            try:
                await bot.load_extension(path)
            except ExtensionError as error:
                log.append((False, error.args[0]))
            else:
                log.append((True, path))
    
    return


async def use_cogs(bot: Bot, path: str, ext: str, method: str) -> list[tuple, str]:
    """Load, reload or unload cogs"""
    extensions, log = [], []

    # Function writing extensions
    def iter_files(directory: str):
        files: list = os.listdir(os.path.join('bot/cogs/', directory))
        extensions.extend(
            [f'bot.cogs.{directory}.' + os.path.splitext(file)[0] for file in files if file.endswith('.py')])

    # Action according to the data
    if path == 'all':
        for path in ('admin', 'user', 'other', 'server'):
            iter_files(path)
    elif path in ('admin', 'user', 'other', 'server'):
        if not ext:
            iter_files(path)
        else:
            extensions.append(f'bot.cogs.{path}.{ext}')
    else:
        raise MissingRequiredArgument

    # Action with cogs themselves
    for cog in extensions:
        try:
            await getattr(bot, f'{method}_extension')(cog)
        except ExtensionError as error:
            log.append(error.args)
        else:
            log.append(cog)

    return log
