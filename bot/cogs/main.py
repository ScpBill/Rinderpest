from discord.ext.commands import Bot

import importlib
manager = importlib.import_module('bot.misc.utils.server')


async def setup_all_cogs(bot: Bot) -> None:
    log = await manager.use_cogs('all', '', bot.load_extension)
    for data in log:
        if isinstance(data, str):
            print(f'[+] Cog «{data}» has been successfully load')
        elif isinstance(data, tuple):
            print('[-] {}'.format(data[0]))
