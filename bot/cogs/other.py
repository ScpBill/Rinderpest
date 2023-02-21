from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction

from bot.misc.config import Config

from git.repo import Repo
from git.exc import GitError
import traceback
import subprocess


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print('[*] Bot is started! [*]')

    @Bot.slash_command(Bot(), 'update')
    async def update(self, interaction: Interaction):
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        reply = await interaction.response.send_message(
            'Please wait...', ephemeral=True
        )

        repo = Repo('./')
        try:
            repo.remotes.origin.pull()
            repo.commit()
        except GitError:
            await reply.edit(traceback.format_exc())
        else:
            await reply.edit('The git repository has been successfully updated!')

    @Bot.slash_command(Bot(), 'cmd')
    async def cmd(self, interaction: Interaction, command: str):
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        reply = await interaction.response.send_message(
            'Please wait...', ephemeral=True
        )
        try:
            output: bytes = subprocess.check_output(command.split(' '))
        except Exception:
            await reply.edit(traceback.format_exc())
        else:
            await reply.edit(output.decode('utf-8'))


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
