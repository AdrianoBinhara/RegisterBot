from discord.ext import commands
import os
from decouple import config

bot = commands.Bot("!")


def load_cogs(bot):
    bot.load_extension("manager")
    ##bot.load_extension("tasks.purge")

    for file in os.listdir("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"commands.{cog}")


load_cogs(bot)

TOKEN = config("TOKEN")
bot.run(TOKEN)
