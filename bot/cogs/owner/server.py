from discord.ext.commands import Cog, Bot, Context
from discord.ext import commands
from discord import app_commands, Message

from bot.spec.config import Config

import subprocess
import typing
import time


class ServerManagement(Cog, name='Server Management', description='Managing the bot\'s command tree',
                       command_attrs=dict(hidden=True, guild_ids=[Config.ID_GUILD])):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.last_call_time = None

    @staticmethod
    def execute(shell: str) -> typing.Generator:
        popen = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for stdout_line in iter(popen.stdout.readline, ''):
            yield stdout_line, None
        if return_code := popen.wait():
            for stderr_line in iter(popen.stderr.readline, ''):
                yield stderr_line, None

        popen.stdout.close()
        popen.stderr.close()
        yield '', return_code

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

    @commands.hybrid_command(
        name='console', aliases=['cmd', 'shell'])
    @commands.is_owner()
    async def _console(self, ctx: Context, *, args: str) -> None:
        await ctx.defer()

        content = executing_text = f'**Executing the command `{args}`:**'
        output_message: Message = await ctx.reply(executing_text, mention_author=False)

        result_generator = self.execute(args)
        for line, code in result_generator:
            line, content = line.replace('``', "`​`"), content

            if code is None:
                if content == executing_text:
                    content += '\n```\n' + line + '```'
                else:
                    content = content[:-3] + line + '```'
                output_message: Message = await self.edit_message_include_cooldown(output_message, content=content)
            else:
                output_message: Message = await output_message.edit(content=content + f'\n**Return code: `{code}`**')

    async def edit_message_include_cooldown(self, message: Message, *, content: str) -> Message:
        cooldown = 0.5

        if (self.last_call_time is None) or (time.time() - self.last_call_time > cooldown):
            self.last_call_time = time.time()

            return await message.edit(content=content)
        return message


async def setup(bot: Bot) -> None:
    await bot.add_cog(ServerManagement(bot))
