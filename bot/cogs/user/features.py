from discord.ext.commands import Cog, Bot, Context, MissingRequiredArgument, EmojiNotFound
from discord import NotFound, Message, Reaction, Member, Embed, Emoji
from discord.ext import commands
from discord import app_commands

import asyncio
import sympy
import sys


FONTS = {
    'regular':                '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
    'bold':                   '𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳',
    'italic':                 '----------𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧',
    'bold-italic':            '----------𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛',
    'script':                 '----------𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏',
    'bold-script':            '----------𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃',
    'fraktur':                '----------𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷',
    'double-struck':          '',
    'bold-fraktur':           '',
    'sans-serif':             '',
    'sans-serif-bold':        '',
    'sans-serif-italic':      '',
    'sans-serif-bold-italic': '',
    'monospace':              ''
}


class FeaturesCogs(Cog, name='Features', description='Other user commands'):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.hybrid_command()
    @app_commands.choices(style=[
        app_commands.Choice(name='𝐁𝐨𝐥𝐝', value='bold'),
        app_commands.Choice(name='𝐼𝑡𝑎𝑙𝑖𝑐', value='italic'),
        app_commands.Choice(name='𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄', value='bold-italic'),
        app_commands.Choice(name='𝒮𝒸𝓇𝒾𝓅𝓉', value='script'),
        app_commands.Choice(name='𝓑𝓸𝓵𝓭 𝓢𝓬𝓻𝓲𝓹𝓽', value='bold-script'),
        app_commands.Choice(name='𝔉𝔯𝔞𝔨𝔱𝔲𝔯', value='fraktur'),
        app_commands.Choice(name='𝔻𝕠𝕦𝕓𝕝𝕖-𝕤𝕥𝕣𝕦𝕔𝕜', value='double-struck'),
        app_commands.Choice(name='𝕭𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗', value='bold-fraktur'),
        app_commands.Choice(name='𝖲𝖺𝗇𝗌-𝗌𝖾𝗋𝗂𝖿', value='sans-serif'),
        app_commands.Choice(name='1', value='sans-serif-bold'),
        app_commands.Choice(name='2', value='sans-serif-italic'),
        app_commands.Choice(name='3', value='sans-serif-bold-italic'),
        app_commands.Choice(name='4', value='monospace')
    ])
    async def font(self, ctx: Context,
                   style: str = commands.parameter(description='Style font of your text, long name is separated with `-`', default='bold fraktur'), *,
                   text: str = commands.parameter(description='Your text')):
        """The font generator: write and copy!"""
        
        # Wait message
        await ctx.defer()
        if style not in FONTS.keys():
            return await ctx.reply('**The font is specified incorrectly.**\n*Available fonts*: %s' % ' '.join([f'`{name}`' for name in FONTS.keys()]))
        
        alphabet, decorated = FONTS['regular'], FONTS[style]
        # Replace symbols
        try:
            await ctx.reply(''.join([decorated[alphabet.index(char)] if
                                     char in alphabet and decorated[alphabet.index(char)] != '-' else char
                                     for char in text]))
        except IndexError:
            await ctx.reply('Sorry, an unintentional error has occured.')

    @font.error
    async def argument_error(self, ctx: Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send_help(ctx.command)


async def setup(bot: Bot) -> None:
    await bot.add_cog(FeaturesCogs(bot))
