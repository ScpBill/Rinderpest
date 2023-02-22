from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction

from bot.misc.config import Config

import os
import sys
from subprocess import check_output


# todo: OtherCogs
class __ServerOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Bot.slash_command(Bot(), 'update')
    async def _update(self, ctx: Interaction):
        """Updating data via a remote git repository"""
        # Check on author is me
        if ctx.user.id != Config.ID_ME:
            await ctx.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.response.defer(ephemeral=True, with_message=True)
        msg, log = 'The progress of reading data from a remote server', []

        # Generate commands
        await ctx.followup.send(
            msg := msg + '\n• Git reset finish the code `{}`'.format(
                code_1 := os.system('git reset --hard')))

        await ctx.followup.send(
            msg := msg + '\n• Git pull finish the code `{}`'.format(
                code_2 := os.system('git pull origin master --no-commit --no-ff')))

        # Main result message
        if all(code == 0 for code in (code_1, code_2)):
            await ctx.followup.send(msg + '\n**The git repository has been successfully updated!**')
        else:
            await ctx.followup.send(msg + '\n**The git repository update failed**')

    @Bot.slash_command(Bot(), 'restart')
    async def _restart(self, ctx: Interaction):
        """Restarting bot"""
        # Check on author is me
        if ctx.user.id != Config.ID_ME:
            await ctx.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Out message
        await ctx.response.send_message(
            'I\'m restarting...', ephemeral=True
        )
        os.execv(sys.executable, ['python'] + sys.argv)

    @Bot.slash_command(Bot(), 'git')
    async def git_cmd(self, ctx: Interaction, args: str):
        """Executing git commands via the bot command"""
        # Check on author is me
        if ctx.user.id != Config.ID_ME:
            await ctx.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        await ctx.response.defer(ephemeral=True, with_message=True)

        # Executing a command and getting data
        output: str = check_output('git ' + args).decode('utf-8')
        if len(output) >= 2000:
            output = '```\n{}\n...\n```'.format(output[:1980])

        # Sending result
        await ctx.followup.send(output)


def setup(bot: Bot) -> None:
    bot.add_cog(__ServerOtherCog(bot))
