# bot.py
from dotenv import dotenv_values
import discord
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix="redis ")
slash = SlashCommand(bot, override_type=True, sync_commands = True)




@bot.command()
async def fetch(ctx, args = None):
    result = discord.Embed(
        title='Fetch:',
        description='<key>: <value>',
        colour=discord.Colour.red()
    )
    await ctx.channel.send(embed=result)


@slash.slash(name="fetch", guild_ids=[428489090162491392], )
async def _fetch(ctx, args = None):
    result = discord.Embed(
        title='Fetch:',
        description='<key>: <value>',
        colour=discord.Colour.red()
    )
    await ctx.channel.send(embed=result)


bot.run(str(dotenv_values("token.env")["TOKEN"]))
