from nextcord.ext.commands import Cog, Bot, ExtensionNotLoaded, ExtensionNotFound, NoEntryPointError, ExtensionFailed, \
    ExtensionAlreadyLoaded, InvalidSetupArguments
from nextcord import Interaction

from bot.misc.config import Config

import os


def _valid_extensions(extensions: str) -> list:
    if not extensions:
        for (dir_path, dir_names, file_names) in os.walk('bot\\cogs'):

            # Add a cog name to the list
            for name in file_names:
                if os.path.splitext(name)[1] == '.py':
                    path: str = dir_path.replace('\\', '.')
                    extensions += (' ' if extensions else '') + f'{path}.{os.path.splitext(name)[0]}'
        return extensions.split(' ')

    else:
        ls = extensions.split(' ')
        for extension in ls:
            assert extension.startswith('cogs.'), 'Invalid argument'
        return ['bot.' + ext for ext in ls]


class __LoaderOtherCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Bot.slash_command(Bot())
    async def reload(self, interaction: Interaction, *, cogs: str = ''):
        """Using for reload the bot cogs. Cogs are separated by space."""
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Logging and Reloading Extension
        log, success = [], 0
        for cog in _valid_extensions(cogs):
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

    @Bot.slash_command(Bot())
    async def load(self, interaction: Interaction, *, cogs: str = ''):
        """Using for reload the bot cogs. Cogs are separated by space."""
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Logging and Reloading Extension
        log, success = [], 0
        for cog in _valid_extensions(cogs):
            try:
                self.bot.load_extension(cog)
            except ExtensionNotFound as exc:
                log.append(exc.args[0])
            except ExtensionAlreadyLoaded as exc:
                log.append(exc.args[0])
            except NoEntryPointError as exc:
                log.append(exc.args[0])
            except ExtensionFailed as exc:
                log.append(exc.args[0])
            except InvalidSetupArguments as exc:
                log.append(exc.args[0])

            else:
                success += 1

        # Outputs a result by reload
        await interaction.response.send_message(
            '**All extensions have been load successfully**' if not log else

            '\n'.join(['• ' + err.replace("'", '`') for err in log])
            + f'\n**Successfully load {success} extensions**',

            ephemeral=True
        )

    @Bot.slash_command(Bot())
    async def unload(self, interaction: Interaction, *, cogs: str = ''):
        """Using for reload the bot cogs. Cogs are separated by space."""
        # Check on author is me
        if interaction.user.id != Config.ID_ME:
            await interaction.response.send_message('You cannot use this command', ephemeral=True)
            return

        # Logging and Reloading Extension
        log, success = [], 0
        for cog in _valid_extensions(cogs):
            try:
                self.bot.unload_extension(cog)
            except ExtensionNotFound as exc:
                log.append(exc.args[0])
            except ExtensionNotLoaded as exc:
                log.append(exc.args[0])

            else:
                success += 1

        # Outputs a result by reload
        await interaction.response.send_message(
            '**All extensions have been unload successfully**' if not log else

            '\n'.join(['• ' + err.replace("'", '`') for err in log])
            + f'\n**Successfully unload {success} extensions**',

            ephemeral=True
        )


def setup(bot: Bot) -> None:
    bot.add_cog(__LoaderOtherCog(bot))
