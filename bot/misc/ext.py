from discord.ext.commands import Bot, ExtensionError, MissingRequiredArgument

import os


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
