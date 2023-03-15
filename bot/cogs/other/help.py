from discord.ext.commands import Bot, HelpCommand, Cog, Group, Command, Context
from discord import Embed, Color

from discord.ext import commands

import importlib
import sys

Config = importlib.import_module('bot.misc.config').Config


class MainHelpCommand(HelpCommand):

    def get_command_signature(self, command: Command) -> str:
        if command.signature:
            return '`%s%s %s`' % (self.context.clean_prefix, command.qualified_name, command.signature)
        return '`%s%s`' % (self.context.clean_prefix, command.qualified_name)

    def get_prefix_command(self, command: Command) -> str:
        return '`%s%s`' % (self.context.clean_prefix, command.qualified_name)

    async def filter_commands(self, list_commands: [list, set], /, *, sort: bool = False, key=None) -> list[Command]:
        importlib.reload(sys.modules[Config.__module__])

        show_hidden = self.context.author.id == Config.ID_ME
        iterator = list_commands if show_hidden else filter(lambda c: not c.hidden, list_commands)

        return sorted(iterator, key=key if key is not None else lambda c: c.name) if sort else list(iterator)

    async def send_bot_help(self, mapping, /) -> None:
        embed = Embed(
            title='Help Information',
            description=
            '''Type `/help` to view the list of commands.
Type `/help <command>` to get detailed information on the command or category.''',
            color=Color.light_grey())

        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            prefix_commands = [self.get_prefix_command(c) for c in filtered]

            if prefix_commands:
                cog_name = getattr(cog, 'qualified_name', 'No Category')
                embed.add_field(name=cog_name, value=' '.join(prefix_commands), inline=True)

        await self.context.reply(embed=embed)

    async def send_cog_help(self, cog: Cog, /) -> None:
        embed = Embed(
            title='Help for "%s" category' % (cog.qualified_name or 'No Category'),
            description=
            '''Type `/help` to view the list of commands.
Type `/help <command>` to get detailed information on the command or category.''',
            color=Color.light_grey())

        embed.add_field(name='Category description', value=cog.description)

        if filtered_commands := await self.filter_commands(cog.get_commands()):
            command_context = [
                '%s — %s' % (self.get_prefix_command(c), c.help or 'No help message found...')
                for c in filtered_commands]

            embed.add_field(name='Available commands', value='\n'.join(command_context), inline=False)

        await self.context.reply(embed=embed)

    async def send_group_help(self, group: Group, /) -> None:
        embed = Embed(
            title='Help for "%s" group' % group.qualified_name,
            description=
            '''Type `/help` to view the list of commands.
Type `/help <command>` to get detailed information on the command or category.''',
            color=Color.light_grey())

        embed.add_field(name='Group description', value=group.help)
        embed.add_field(name='Group signature', value=self.get_command_signature(group))

        if filtered_commands := await self.filter_commands(group.commands):
            command_context = [
                '%s — %s' % ('`{}`'.format(c.qualified_name), c.help or 'No help message found...')
                for c in filtered_commands]

            embed.add_field(name='Commands', value='\n'.join(command_context), inline=False)

        await self.context.reply(embed=embed)

    async def send_command_help(self, command: Command, /) -> None:
        embed = Embed(
            title='Help for "%s" command' % command.qualified_name,
            description=
            '''Type `/help` to view the list of commands.
Type `/help <command>` to get detailed information on the command or category.''',
            color=Color.light_grey())

        embed.add_field(name='Command description', value=command.help)
        embed.add_field(name='Command signature', value=self.get_command_signature(command))

        if params := command.params:
            param_context = []
            for name, parameter in params.items():
                param_context.append('%s — %s' % (name, parameter.description))
            embed.add_field(name='Attributes', value='\n'.join(param_context), inline=False)
        if alias := command.aliases:
            embed.add_field(name='Aliases', value=', '.join(alias), inline=False)

        await self.context.reply(embed=embed)

    async def send_error_message(self, error: str, /) -> None:
        embed = Embed(
            title="Error in help",
            description=
            '''Type `/help` to view the list of commands.
Type `/help <command>` to get detailed information on the command or category.''',
            color=Color.red())

        embed.add_field(name='Error name', value=error)

        await self.context.reply(embed=embed)

    async def command_not_found(self, string: str, /) -> str:
        return f'Command `{string}` not found.'


class SlashHelpCommands(Cog, name='Help Information', description='Get a help about commands'):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.help_command = MainHelpCommand()
        self.bot.remove_command('help')

    @commands.hybrid_command(name='help')
    async def _help(self, ctx: Context, *, command: str = commands.parameter(
                    description='Either name of command/group or name of category', default=None)):
        """Show the list of all commands and all categories and they description, syntax, arguments"""

        if command is not None:
            await ctx.send_help(command)
        else:
            await ctx.send_help()


async def setup(bot: Bot) -> None:
    await bot.add_cog(SlashHelpCommands(bot))
