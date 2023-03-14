from discord.ext.commands import Bot
from discord.utils import get
from discord import Emoji
from emoji_list import all_emoji

import re


def get_emoji(bot: Bot, data: str) -> [Emoji, str, None]:
    if get(bot.emojis, name=data):  # Emoji
        emoji = get(bot.emojis, name=data)
    elif data.isnumeric():  # ID
        emoji = bot.get_emoji(int(data))
    elif re.fullmatch(r'(:\w+:)|(<\w*:\w+:\w+>)', data):  # :emoji: | <*a:emoji:id>
        emoji = get(bot.emojis, name=data.split(':')[1])
    elif isinstance(data, str):  # Standard
        emoji = data if data in all_emoji else None
    else:
        emoji = None
    return emoji
