from nextcord.ext.commands import Bot
import os


def setup_admin_cogs(bot: Bot) -> None:
    """Setup cogs by loading extensions"""
    extensions: list = os.listdir('bot\\cogs\\admin\\')
    extensions.remove('__init__.py')

    bot.load_extensions(extensions)
