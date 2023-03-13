from discord.ext.commands import Cog, Bot, Context, MissingRequiredArgument, EmojiNotFound
from discord import NotFound, Message, Reaction, Member, Embed
from discord.ext import commands
from discord.utils import get

import asyncio
import re
import sympy


# todo: UserCogs
class __MainUserCog(Cog, name='General', description='Basic user commands'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: Context) -> None:
        """Simple command that responds with Pong!"""
        await ctx.send('Pong!')

    @commands.hybrid_command(aliases=('reaction', 'send_emoji', 'rs'))
    async def send_reaction(self, ctx: Context, emoji: str, id_message: str = None):
        """Puts a reaction to the specified message so that after, the author clicks on it"""

        def check(this_reaction: Reaction, this_user: Member):
            return this_reaction.message == current_message and this_reaction.emoji == emoji and this_user == ctx.author

        # Waiting message
        await ctx.defer(ephemeral=True)
        if not ctx.interaction:
            await ctx.message.delete()

        # Getting emoji
        if get(self.bot.emojis, name=emoji):  # Emoji
            emoji = get(self.bot.emojis, name=emoji)
        elif emoji.isnumeric():  # ID
            emoji = self.bot.get_emoji(int(emoji))
        elif re.fullmatch(r'(:\w+:)|(<\w*:\w+:\w+>)', emoji):  # :emoji: | <*a:emoji:id>
            emoji = get(self.bot.emojis, name=emoji.split(':')[1])
        elif isinstance(emoji, str):  # Standard
            pass
        else:
            await ctx.send(r'Sorry, could not find the specified emoji. ¯\_(ツ)_/¯', ephemeral=True)
            return

        # Get a current message id
        if id_message is None and ctx.message.reference:
            id_message = ctx.message.reference.message_id

        # And get a current message
        try:
            assert id_message is not None
            current_message: Message = await ctx.fetch_message(int(id_message))
        except AssertionError:
            current_message: Message = [msg async for msg in ctx.channel.history(limit=1)].pop(0)
        except NotFound:
            await ctx.reply('Did not find the specified message', ephemeral=True, delete_after=10.0)
            return

        # Add reaction to message
        try:
            await current_message.add_reaction(emoji)
        except NotFound:
            await ctx.send(r'Sorry, could not find the specified emoji. ¯\_(ツ)_/¯', ephemeral=True)
            return
        except TypeError:
            await ctx.send(r'Sorry, could not find the specified emoji. ¯\_(ツ)_/¯', ephemeral=True)
            return

        if ctx.interaction:
            await ctx.reply('Emoji successfully added', ephemeral=True)

        # Wait author click on reaction
        try:
            await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            pass

        # Remove my self reaction
        await current_message.remove_reaction(emoji, self.bot.user)

    @commands.hybrid_command(aliases=('calc', 'math'))
    async def calculator(self, ctx: Context, *,
                         expression: str = commands.parameter(description='String with the expression')):
        """Calculating a mathematical expression"""

        # Wait message
        await ctx.defer()

        # Expressing
        try:
            expr: sympy.Expr | str = sympy.parse_expr(
                expression, evaluate=True, transformations=sympy.parsing.sympy_parser.standard_transformations)
        except Exception as error:
            expr, result = type(error).__name__, type(error).__name__
        else:
            try:
                result = expr.evalf(30)
            except Exception as error:
                result = type(error).__name__

        # Output
        embed = Embed(title='Math Calculator', description='Based on SymPy')
        embed.add_field(name='Your expression:', value='```py\n%s\n```' % expression, inline=False)
        if expr != result:
            embed.add_field(name='Simplified view:', value='```py\n%s\n```' % expr)
        embed.add_field(name='Result:', value='```py\n%s\n```' % result)
        embed.set_author(name='by %s' % ctx.author.display_name, icon_url=ctx.author.avatar.url)

        # Send
        await ctx.send(embed=embed)

    @send_reaction.error
    @calculator.error
    async def argument_error(self, ctx: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        else:
            await ctx.reply(error)

    @send_reaction.error
    async def send_reaction_error(self, ctx: Context, error):
        if isinstance(error, EmojiNotFound):
            if not ctx.interaction:
                await ctx.message.delete()
            await ctx.send(r'Sorry, could not find the specified emoji. ¯\_(ツ)_/¯', ephemeral=True)
        elif not isinstance(error, MissingRequiredArgument):
            await self.bot.get_channel(1082725745920589954).send('```\n%s\n```' % error)


async def setup(bot: Bot) -> None:
    await bot.add_cog(__MainUserCog(bot))
