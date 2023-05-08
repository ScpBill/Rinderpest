from discord.ext.commands import Cog, Bot, Context
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, CheckFailure

from bot.spec.config import Config

import traceback


class ErrorHandler(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(error, CommandNotFound):
            await ctx.send_help() if ctx.clean_prefix != Config.CMD_PREFIX else ...
        elif isinstance(error, CheckFailure):
            await ctx.reply(error.__str__())
        else:
            traceback.print_exception(type(error), error, error.__traceback__)


async def setup(bot: Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
