# bot.py
from dotenv import dotenv_values
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix="prefix")
slash = SlashCommand(bot, override_type=True)


bot.load_extension("cog")
bot.run(str(dotenv_values("token.env")["TOKEN"]))
