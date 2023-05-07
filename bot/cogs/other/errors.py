from discord.ext.commands import Cog, Bot, Context
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument

from bot.spec.config import Config

import traceback


class ErrorHandler(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send_help(ctx.command)
        elif isinstance(error, CommandNotFound):
            return await ctx.send_help() if ctx.clean_prefix != Config.CMD_PREFIX else ...
        else:
            traceback.print_exception(type(error), error, error.__traceback__)


async def setup(bot: Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
