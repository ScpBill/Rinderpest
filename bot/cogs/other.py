from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction
from git.repo import Repo
from git.exc import GitError


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print('[*] Bot is started! [*]')

    @Bot.slash_command(Bot(), 'update')
    async def update(self, interaction: Interaction):
        reply = await interaction.response.send_message(
            'Please wait...', ephemeral=True
        )

        repo = Repo('./')
        try:
            repo.remotes.origin.pull()
        except GitError:
            await reply.edit('The git repository __has already been updated__ or an unexpected error has occurred.')
        else:
            await reply.edit('The git repository has been successfully updated!')


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
