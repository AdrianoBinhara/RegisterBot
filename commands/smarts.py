from discord.ext import commands


class Smart(commands.Cog):
    """Smart Commands"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Smart(bot))
