from discord.ext.commands import Cog, Bot, Context
from discord.ext import commands
from discord import app_commands

from bot.spec.config import Config

import subprocess
import typing


class ServerManagement(Cog, name='Server Management', description='Managing the bot\'s command tree',
                       command_attrs=dict(hidden=True, guild_ids=[Config.ID_GUILD])):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command(
        name='update', description='Updating project files using the GitHub repository',
        help='Specify arguments with extreme caution', usage='update [before_invoke] [invoke_commands] [after_invoke]')
    @app_commands.describe(
        before_invoke='Commands executed __before__ calling the update, are separated by `;`',
        after_invoke='Commands executed __after__ calling the update, are separated by `;`'
    )
    @commands.is_owner()
    async def _update(self, ctx: Context, *, before_invoke: str = '', after_invoke: str = '') -> None:
        await ctx.defer()
        output_message = await ctx.reply('OUTPUT')

        def execute(shell: str) -> typing.Generator:
            popen = subprocess.Popen(shell, stdout=subprocess.PIPE, universal_newlines=True)
            for stdout_line in iter(popen.stdout.readline, ''):
                yield stdout_line
            popen.stdout.close()
            if return_code := popen.wait():
                raise subprocess.CalledProcessError(return_code, shell)

        for line in execute(before_invoke):
            await output_message.edit(content=output_message.content + f'\n{line}')


async def setup(bot: Bot) -> None:
    await bot.add_cog(ServerManagement(bot))
