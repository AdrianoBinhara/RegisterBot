from discord.ext import commands, tasks


class Purge(commands.Cog):
    """Work over time"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        purgue_time.start(self)


@tasks.loop(seconds=45)
async def purgue_time(self):
    channel = self.bot.get_channel(774813806844575757)

    count = 0
    async for _ in channel.history(limit=None):
        count += 1

    if count > 0:
        await channel.purge(limit=10)


def setup(bot):
    bot.add_cog(Purge(bot))
