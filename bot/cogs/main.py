from discord.ext.commands import Bot


async def setup_all_cogs(bot: Bot) -> None:
    use_cogs = getattr(bot.get_cog('ManageServer'), 'use_cogs')
    log = await use_cogs('all', '', bot.load_extension)
    for data in log:
        if isinstance(data, str):
            print(f'[+] Cog «{data}» has been successfully load')
        elif isinstance(data, tuple):
            print('[-] {}'.format(data[0]))
