from discord.enums import ButtonStyle
from discord.ui import View, Button, Item
from discord import Interaction, Message

from discord import ui

import textwrap


class PagesView(View):
    children: list[Button]

    def __init__(self, *, text: str, timeout=180):
        super().__init__(timeout=timeout)
        self.pages = textwrap.wrap(text, 1988)  # [```\n{x\n...}\n```]:  x == 1988 + 4 + 8  ==>  x == 1992 + 8
        self.current_page = 0

    @ui.button(label='', disabled=True, style=ButtonStyle.gray, emoji='←')
    async def back_page(self, button: Button, interaction: Interaction):
        postfix = '\n...'

        if self.current_page > 0:  # page is not first
            self.current_page -= 1

            for b in self.children:
                if b.emoji == '→' and b.disabled:
                    b.disabled = False

        if self.current_page == 0:  # page is first
            button.disabled = True

        await interaction.message.edit(content='```\n{}\n```'.format(self.pages[self.current_page] + postfix))

    @ui.button(label='', disabled=False, style=ButtonStyle.gray, emoji='→')
    async def next_page(self, button: Button, interaction: Interaction):
        postfix = '\n...'

        if self.current_page < len(self.pages) - 1:  # page is not last
            self.current_page += 1

            for b in self.children:
                if b.emoji == '←' and b.disabled:
                    b.disabled = False

        if self.current_page == len(self.pages) - 1:  # page is last
            button.disabled = True
            postfix = ''

        await interaction.message.edit(content='```\n{}\n```'.format(self.pages[self.current_page] + postfix))

