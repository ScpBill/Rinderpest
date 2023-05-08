from discord.ext.commands import Cog, Bot, Context
from discord.ext import commands
from discord import app_commands, Message

from bot.spec.config import Config

import subprocess
import typing
import time


class Console:
    def __init__(self):
        self.title = '**Executing the command `{args}`:**'
        self.footer = '**Return code: `{code}`**'
        self.content = ''
        self.args = None
        self.code = None
        self.last_call_time = None

    @staticmethod
    def _execute(shell: str) -> typing.Generator:
        popen = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                 shell=True)

        for stdout_line in iter(popen.stdout.readline, ''):
            yield stdout_line, None
        if return_code := popen.wait():
            for stderr_line in iter(popen.stderr.readline, ''):
                yield stderr_line, None

        popen.stdout.close()
        popen.stderr.close()
        yield '', return_code

    async def run_execution(self, ctx: Context, *, args: str) -> None:
        self.args = args

        replied_msg: Message = await ctx.reply(self.message, mention_author=False)
        result_generator = self._execute(self.args)

        for line, code in result_generator:
            string_with_new_line = line.replace('``', "`​`")

            if code is None:
                self.content += string_with_new_line
            else:
                self.code = code

            await self._edit_message_include_cooldown(
                message=replied_msg, content=self.message, necessarily=self.code is not None)

    @property
    def message(self) -> str:
        title = f'{self.title.format(args=self.args)}\n' if self.args is not None else ''
        footer = f'\n{self.footer.format(code=self.code)}' if self.code is not None else ''

        # len(title) +\n+ len(```) +\n+ ~len(content)~ + len(```) +\n+ len(footer) < 2000
        accept_length = 2000 - len(title) - len(footer) - 7  # other chars
        if len(self.content) > accept_length:  # end content have new line
            accept_length -= 4  # \n...

        cut_content = ''
        if len(self.content) > accept_length:  # 2542 > 1970
            for line in self.content.split('\n'):  # cut for lines
                cut_content += line if not cut_content else f'\n{line}'  # add new line or not

                if len(cut_content) > accept_length:  # stop add lines
                    cut_content = cut_content[:-len(line)]  # remove last line
                    break
            cut_content += '...'
        elif self.content:  # 456 > 0
            cut_content = self.content

        return f'{title}```\n{cut_content}\n```{footer}' if cut_content else f'{title[:-1]}{footer}'

    async def _edit_message_include_cooldown(
            self, message: Message, *, content: str, necessarily: bool = False) -> Message:
        cooldown = 0.5

        if (self.last_call_time is None) or (time.time() - self.last_call_time > cooldown) or necessarily:
            self.last_call_time = time.time()

            return await message.edit(content=content)
        return message


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

    @commands.hybrid_command(
        name='console', aliases=['cmd', 'shell'])
    @commands.is_owner()
    async def _console(self, ctx: Context, *, args: str) -> None:
        await ctx.defer()

        console = Console()
        await console.run_execution(ctx, args=args)


async def setup(bot: Bot) -> None:
    await bot.add_cog(ServerManagement(bot))
