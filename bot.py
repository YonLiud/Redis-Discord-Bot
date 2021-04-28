
from dotenv import dotenv_values
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from datetime import datetime
import re


now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


bot = commands.Bot(command_prefix="redis ")
slash = SlashCommand(bot, override_type=True, sync_commands = True)

guild_ids=[428489090162491392]

# @bot.command()
# async def fetch(ctx, args = None):
#     result = discord.Embed(
#         title='Fetch:',
#         description='<key>: <value>',
#         colour=discord.Colour.red()
#     )
#     await ctx.channel.send(embed=result)


@slash.slash(name="config", description="Edit `config.env` file",  guild_ids=guild_ids, options=[
                create_option(
                 name="option",
                 description="Ed",
                 option_type=3,
                 required=True,

                 choices=[
                    create_choice(
                        name="Hostname",
                        value="hostname"
                    ),
                    create_choice(
                        name="Port",
                        value="port"
                    ),
                     create_choice(
                         name="Database",
                         value="db"
                    )

                 ])
             ])
async def _config(ctx, option):
    msg = ""
    def check_int(m):
        try:
            val = int(m.content)
            return True
        except ValueError:
            return False
    def check_ip(m):
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        x = (re.search(regex, m.content))
        return x
    await ctx.send(f"Chosen: {option}")
    try:
        if option == "db":
            await ctx.send(f"Select new database index (MUST BE NUMBER)")
            msg = await bot.wait_for("message")
            if not (check_int(msg)):
                raise Exception("Invalid Input")
        elif option == "port":
            await ctx.send(f"Select new port for Redis-bot (MUST BE NUMBER)")
            msg = await bot.wait_for("message")
            if not (check_int(msg)):
                raise Exception("Invalid Input")
        elif option == "hostname":
            await ctx.send(f"Select new IP Address for Redis-bot (MUST BE VALID IP)")
            msg = await bot.wait_for("message")
            if not (check_ip(msg)):
                raise Exception("Invalid Input")
        await ctx.send(f"Changing `{option}` to `{msg.content}`")
    except Exception as e:
        await ctx.send(f"**An error has occurred**! Exception: ``{e}``")



@slash.slash(name="set", description="Execute `set`", guild_ids=guild_ids, )
async def _set(ctx, key, value):
    now = datetime.now()  # current date and time
    result = discord.Embed(
        title='Set:',
        description=f'Exec time: {now}\n\n``{key}``: ``{value}``',
        colour=discord.Colour.red()
    )
    await ctx.send(embed=result)


@slash.slash(name="get", description="Execute `get`", guild_ids=guild_ids, )
async def _get(ctx, key):
    now = datetime.now()  # current date and time
    result = discord.Embed(
        title='Get:',
        description=f'Exec time: {now}\n\n``{key}``: ``<value>``',
        colour=discord.Colour.red()
    )
    await ctx.send(embed=result)


@bot.event
async def on_ready():
    print(f"bot | Launch Time:  ", date_time)
    print(f"Bot | Status:     Operational")
    print(f"Bot | ID:         {format(bot.user.id)}")
    print(f"Bot | Name:       {format(bot.user.name)}")
    print(f"Bot is ready to use")

bot.run(str(dotenv_values("token.env")["TOKEN"]))
