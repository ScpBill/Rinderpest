from discord.ext.commands import Bot, HelpCommand, Cog, Group, Command
from discord import Embed, Color


class MainHelpCommand(HelpCommand):

    def get_command_signature(self, command):
        return '`%s%s %s`' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping, /) -> None:
        embed = Embed(title="Help", color=Color.light_grey())

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]

            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        await self.context.reply(embed=embed)

    async def send_cog_help(self, cog: Cog, /) -> None:
        embed = Embed(title=cog.qualified_name or "No Category", description=cog.description, color=Color.light_grey())

        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command),
                                value=command.help or "No Help Message Found... ")

        await self.context.reply(embed=embed)

    async def send_group_help(self, group: Group, /) -> None:
        embed = Embed(title=self.get_command_signature(group), description=group.help, color=Color.light_grey())

        if filtered_commands := await self.filter_commands(group.commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command),
                                value=command.help or "No Help Message Found... ")

        await self.context.reply(embed=embed)

    async def send_command_help(self, command: Command, /) -> None:
        embed = Embed(title=self.get_command_signature(command), color=Color.light_grey())
        if command.help:
            embed.description = command.help
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        await self.context.reply(embed=embed)

    async def send_error_message(self, error: str, /) -> None:
        embed = Embed(title="Error", description=error, color=Color.red())

        await self.context.reply(embed=embed)

    async def command_not_found(self, string: str, /) -> str:
        return f'Command `{string}` not found.'


class SlashHelpCommands(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.help_command = MainHelpCommand()


async def setup(bot: Bot) -> None:
    await bot.add_cog(SlashHelpCommands(bot))
