from nextcord.ext.commands import Bot, Cog, ExtensionNotFound, ExtensionNotLoaded, ExtensionFailed, NoEntryPointError
from nextcord import Interaction
import os
from bot.misc import Config


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print('I am ready!!!')

    @Bot.slash_command(Bot())
    async def reload(self, interaction: Interaction, *, cogs: str = ''):
        """Using for reload the bot cogs. Cogs are separated by space."""
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Finding cogs
        if not cogs:
            for (dir_path, dir_names, file_names) in os.walk('./bot/cogs/'):

                # Add a cog name to the list
                for name in file_names:
                    if os.path.splitext(name)[1] == '.py':
                        path = dir_path[6:].replace('/', '.')
                        cogs += ' ' if cogs else '' + f'{path}.{os.path.splitext(name)[0]}'

        # Logging and Reloading Extension
        log, success = [], 0
        for cog in cogs.split(' '):
            try:
                self.bot.reload_extension(cog)
            except ExtensionNotLoaded as exc:
                log.append(exc.args[0])
            except ExtensionNotFound as exc:
                log.append(exc.args[0])
            except NoEntryPointError as exc:
                log.append(exc.args[0])
            except ExtensionFailed as exc:
                log.append(exc.args[0])

            else:
                success += 1

        # Outputs a result by reload
        await interaction.response.send_message(
            '**All extensions have been reload successfully**' if not log else

            '\n'.join(['• ' + err.replace("'", '`') for err in log])
            + f'\n**Successfully reload {success} extensions**',

            ephemeral=True
        )


def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
