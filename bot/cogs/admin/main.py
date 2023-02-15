from nextcord.ext.commands import Cog, Bot, command


# todo: AdminCogs
class __MainAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def make_channel(self, ctx):
        guild = ctx.guild
        channel = await guild.create_text_channel('secret')


def register_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__MainAdminCog(bot))
