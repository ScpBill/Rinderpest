from discord.ext.commands import Bot

from bot.misc.ext import use_cogs


async def setup_all_cogs(bot: Bot) -> None:
    log = await use_cogs(bot, 'all', '', 'load')
    for data in log:
        if isinstance(data, str):
            print(f'[+] Cog «{data}» has been successfully load')
        elif isinstance(data, tuple):
            print('[-] {}'.format(data[0]))
