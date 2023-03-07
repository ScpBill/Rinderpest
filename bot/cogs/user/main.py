from discord.ext.commands import Cog, Bot, Context
from discord import Emoji, NotFound, Message, Reaction, Member
from discord.ext import commands

import asyncio


# todo: UserCogs
class __MainUserCog(Cog, name='General', description='Basic user commands'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: Context) -> None:
        """Simple command that responds with Pong!"""
        await ctx.send('Pong!')

    @commands.hybrid_command(name='reaction', aliases=('reaction', 'react', 'emoji', 'rs'))
    async def _reaction(self, ctx: Context, emoji: Emoji, id_message: int = 0):
        """Puts a reaction to the specified message so that after, the author clicks on it"""

        def check(this_reaction: Reaction, this_user: Member):
            return this_reaction.message == current_message and this_reaction.emoji == emoji and this_user == ctx.author

        # Get a current message id
        if not id_message and ctx.message.reference:
            id_message = ctx.message.reference.message_id

        # And get a current message
        try:
            assert id_message != 0
            current_message: Message = await ctx.fetch_message(id_message)
        except AssertionError:
            current_message: Message = [msg async for msg in ctx.channel.history(limit=2, oldest_first=False)].pop(1)
        except NotFound:
            await ctx.reply('Did not find the specified message')
            return

        # Add reaction and wait user
        await current_message.add_reaction(emoji)
        await ctx.message.delete()
        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass

        # Remove my self reaction
        await current_message.remove_reaction(emoji, self.bot.user)


async def setup(bot: Bot) -> None:
    await bot.add_cog(__MainUserCog(bot))
