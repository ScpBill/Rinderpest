from discord.ext.commands import Bot, Cog
from discord.enums import ButtonStyle
from discord.ui import View, Button
from discord import Interaction, Emoji

from discord import ui, utils
from emoji_list import all_emoji

import re


class ManageChat(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_emoji(self, data: str) -> [Emoji, str, None]:
        if utils.get(self.bot.emojis, name=data):  # Emoji
            emoji = utils.get(self.bot.emojis, name=data)
        elif data.isnumeric():  # ID
            emoji = self.bot.get_emoji(int(data))
        elif re.fullmatch(r'(:\w+:)|(<\w*:\w+:\w+>)', data):  # :emoji: | <*a:emoji:id>
            emoji = utils.get(self.bot.emojis, name=data.split(':')[1])
        elif isinstance(data, str) and re.match(r'^(?:http|ftp)s?://', data):
            emoji = utils.get(self.bot.emojis, url=data)
        elif isinstance(data, str):  # Standard
            emoji = data if data in all_emoji else None
        else:
            emoji = None
        return emoji

    @staticmethod
    def segments_text(text: str, max_length: int) -> list[str]:
        segments = ['']
        for line in text.split('\n'):
            if len(segments[-1]) + 1 + len(line) <= max_length:
                segments[-1] += '\n%s' % line
            else:
                if not segments[-1]:
                    segments.pop()
                segments.extend([line[s:s + max_length] for s in range(0, len(line), max_length)])
        return segments

    class PagesView(View):
        children: list[Button]

        def __init__(self, *, text: str, timeout=180):
            super().__init__(timeout=timeout)

            # [```\n{x\n...}\n```]:  x == 1988 + 4 + 8  ==>  x == 1992 + 8
            self.pages = ManageChat.segments_text(text, 1988)
            self.current_page = 0

            count_button = [b for b in self.children if b.custom_id == 'count'].pop()
            count_button.label = '{} / {}'.format(self.current_page + 1, len(self.pages))

        @ui.button(label='', disabled=True, style=ButtonStyle.gray, emoji='⬅', custom_id='back')
        async def back_page(self, interaction: Interaction, button: Button):
            postfix = '\n...'

            if self.current_page > 0:  # page is not first
                self.current_page -= 1
                other_button = [b for b in self.children if b.custom_id == 'next'].pop()
                other_button.disabled = False

            if self.current_page == 0:  # page is first
                button.disabled = True

            count_button = [b for b in self.children if b.custom_id == 'count'].pop()
            count_button.label = '{} / {}'.format(self.current_page + 1, len(self.pages))

            await interaction.response.edit_message(
                content='```\n{}\n```'.format(self.pages[self.current_page] + postfix), view=self)

        @ui.button(label='0 / 0', disabled=True, style=ButtonStyle.gray, custom_id='count')
        async def count_page(self, interaction: Interaction, button: Button):
            pass

        @ui.button(label='', disabled=False, style=ButtonStyle.gray, emoji='➡', custom_id='next')
        async def next_page(self, interaction: Interaction, button: Button):
            postfix = '\n...'

            if self.current_page < len(self.pages) - 1:  # page is not last
                self.current_page += 1
                other_button = [b for b in self.children if b.custom_id == 'back'].pop()
                other_button.disabled = False

            if self.current_page == len(self.pages) - 1:  # page is last
                button.disabled = True
                postfix = ''

            count_button = [b for b in self.children if b.custom_id == 'count'].pop()
            count_button.label = '{} / {}'.format(self.current_page + 1, len(self.pages))

            await interaction.response.edit_message(
                content='```\n{}\n```'.format(self.pages[self.current_page] + postfix), view=self)


async def setup(bot: Bot):
    await bot.add_cog(ManageChat(bot))
