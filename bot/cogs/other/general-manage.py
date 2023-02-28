from discord.ext.commands import Bot, Cog, Context, MissingRequiredArgument
from discord.app_commands.models import AppCommand
from discord import Object, Message

from discord.ext import commands

from bot.misc.config import Config

import os
import sys
from subprocess import check_output, CalledProcessError
import shlex


class ServerCog(Cog, name='Server manager', description='Version control of the remote bot'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='update', hidden=True)
    async def _update(self, ctx: Context) -> None:
        """Updating data via a remote git repository"""
        # Check on author is me
        if ctx.author.id != Config.ID_ME:
            await ctx.send('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        msg, log = 'The progress of reading data from a remote server...', []
        reply: Message = await ctx.reply(content=msg, ephemeral=True)

        # Generate commands
        await reply.edit(content=(
            msg := msg + '\n• Git reset finish the code `{}`'.format(
                code_1 := os.system('git reset --hard'))))

        await reply.edit(content=(
            msg := msg + '\n• Git pull finish the code `{}`'.format(
                code_2 := os.system('git pull origin master'))))

        # Main result message
        if all(code == 0 for code in (code_1, code_2)):
            await reply.edit(content=(msg + '\n**The git repository has been successfully updated!**'))
        else:
            await reply.edit(content=(msg + '\n**The git repository update failed**'))

    @commands.command(name='restart', hidden=True)
    async def _restart(self, ctx: Context) -> None:
        """Restarting bot"""
        # Check on author is me
        if ctx.author.id != Config.ID_ME:
            await ctx.send('You cannot use this command', ephemeral=True)
            return

        # Out message
        await ctx.reply(
            'I\'m restarting...', ephemeral=True
        )
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(name='git', hidden=True)
    async def git_cmd(self, ctx: Context, *,
                      args: str = commands.parameter(description='Command Line Arguments')) -> None:
        """Executing git commands via the bot command"""
        # Check on author is me
        if ctx.author.id != Config.ID_ME:
            await ctx.send('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.defer(ephemeral=True)

        # Executing a command and getting data
        try:
            output: str = check_output(shlex.split('git ' + args)).decode('utf-8')
        except CalledProcessError as error:
            output: str = 'Error running command: "{}" see above shell error\nReturn code: {}\n{}'.format(
                error.cmd, error.returncode, error.output.decode('utf-8')
            )

        # Cut the output if he is bigger then 2000 chars
        if len(output) >= 1993:
            output = '{}\n...'.format(output[:1988])  # [x = len(output)]:  x == 1988 + 4  ==>  x == 1992

        # Sending result
        await ctx.reply(content='```\n{}\n```'.format(output))  # [x = len(output)]:  x <= 1992 + 8  ==>  x <= 2000

    @git_cmd.error
    async def git_cmd_error(self, ctx: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send_help(ctx.command)


class ApplicationCog(Cog, name='Bot Manager', description='Managing the work of the bot'):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = Object(id=Config.ID_GUILD)

    @commands.command(name='sync', hidden=True)
    async def _sync(self, ctx: Context) -> None:
        """Synchronization of slash commands"""
        # Check on author is me
        if ctx.author.id != Config.ID_ME:
            await ctx.send('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.defer(ephemeral=True)

        # Synchronization
        self.bot.tree.copy_global_to(guild=self.guild)
        success_commands: list[AppCommand] = await self.bot.tree.sync(guild=self.guild)

        # Compilation of the result message
        msg = '**The result of the synchronization command:**\n'
        msg = msg + '\n'.join(['• The `{}` command has been successfully loaded'.format(
            command.name) for command in success_commands])

        # Outputs a result by sync
        await ctx.reply(msg)


async def setup(bot: Bot) -> None:
    await bot.add_cog(ServerCog(bot))
    await bot.add_cog(ApplicationCog(bot))
