from nextcord.ext.commands import Bot

from bot.cogs.admin import setup_admin_cogs
from bot.cogs.other import setup_other_cogs
from bot.cogs.user import setup_user_cogs


def setup_all_cogs(bot: Bot) -> None:
    cogs = (
        setup_user_cogs,
        setup_admin_cogs,
        setup_other_cogs,
    )
    for cog in cogs:
        cog(bot)
