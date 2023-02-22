from nextcord.ext.commands import Bot
import os


def setup_user_cogs(bot: Bot) -> None:
    """Setup cogs by loading extensions"""
    files: list = os.listdir('./bot/cogs/user/')
    files.remove('__init__.py')

    bot.load_extensions([f'bot.cogs.user.' + os.path.splitext(file)[0] for file in files if file.endswith('.py')])
