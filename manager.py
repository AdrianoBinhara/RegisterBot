from discord.ext import commands


class Manager(commands.Cog):
    """Smart Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Estou pronto! Estou conectado como {self.bot.user}")


def setup(bot):
    bot.add_cog(Manager(bot))
