from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction

from bot.misc.config import Config

import traceback
import subprocess
import os


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print('[*] Bot is started! [*]')

    @Bot.slash_command(Bot(), 'update')
    async def update(self, interaction: Interaction):
        """Updating data via a remote git repository"""
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Waiting message
        reply = await interaction.response.send_message(
            'Please wait...', ephemeral=True
        )
        msg, log = 'The progress of reading data from a remote server', []

        # Generate commands
        await reply.edit(
            msg := msg + '\n• Git reset finish the code `{}`'.format(
                code_1 := os.system('git reset --hard')))

        await reply.edit(
            msg := msg + '\n• Git clean finish the code `{}`'.format(
                code_2 := os.system('git clean -xdf')))

        await reply.edit(
            msg := msg + '\n• Git pull origin finish the code `{}`'.format(
                code_3 := os.system('git pull origin master')))

        # Main result message
        if all(code == 0 for code in (code_1, code_2, code_3)):
            await reply.edit(msg + '\n**The git repository has been successfully updated!**')
        else:
            await reply.edit(msg + '\n**The git repository update failed**')


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
