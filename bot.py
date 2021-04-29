import os
import re
import sys
from datetime import datetime

import discord
import dotenv
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from dotenv import dotenv_values

now = datetime.now()  # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

whitelisted = dotenv_values("config.env")["whitelisted"].split(",")
bot = commands.Bot(command_prefix="redis ")
slash = SlashCommand(bot, override_type=True, sync_commands=True)

guild_ids = [int(dotenv_values("config.env")["guild_id"])]


async def env_adj(key, value):
    dotenv.set_key("config.env", str(key).upper(), value)


@slash.slash(name="Reboot", description=f"", guild_ids=guild_ids)
async def _reboot(ctx):
    now = datetime.now()  # current date and time
    result = discord.Embed(
        title='Rebooting',
        description=f'Execution time: {now}\n\n**ATTEMPTING REBOOT**',
        colour=discord.Colour.teal()
    )
    await ctx.send(embed=result)
    try:
        if str(ctx.author.id) not in whitelisted:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
        output = "Verification Complete!\nRebooting..."
    except Exception as e:
        output = f"**An error has occurred**! Exception: ``{e}``"
        if str(e).startswith("01 "):
            output += "\n***🔴🔴This incident will be reported!🔴🔴***"
        await ctx.send(output)
    else:
        await ctx.send(output)
        try:
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            output = f"**An error has occurred**! Exception: ``{e}`` at {now}"
            await ctx.message.delete()
            await ctx.send(output)


@slash.slash(name="config", description="Edit `config.env` file", guild_ids=guild_ids, options=[
    create_option(
        name="option",
        description="Ed",
        option_type=3,
        required=True,

        choices=[
            create_choice(
                name="Hostname",
                value="HOSTNAME"
            ),
            create_choice(
                name="Port",
                value="PORT"
            ),
            create_choice(
                name="Database",
                value="DB"
            )

        ])
])
async def _config(ctx, option):
    msg = ""

    def check_int(m):
        try:
            int(m.content)
            return True
        except ValueError:
            return False

    def check_ip(m):
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        x = (re.search(regex, m.content))
        return x

    try:
        if option == "DB":
            await ctx.send(f"Select new database index (MUST BE NUMBER)")
            msg = await bot.wait_for("message")
            await ctx.message.delete()
            if not (check_int(msg)):
                raise Exception("00 Invalid Input")
        elif option == "PORT":
            await ctx.send(f"Select new port for Redis-bot (MUST BE NUMBER)")
            msg = await bot.wait_for("message")
            await ctx.message.delete()
            if not (check_int(msg)):
                raise Exception("00 Invalid Input")
        elif option == "HOSTNAME":
            await ctx.send(f"Select new IP Address for Redis-bot (MUST BE VALID IP)")
            msg = await bot.wait_for("message")
            await ctx.message.delete()
            if not (check_ip(msg)):
                raise Exception("00 Invalid Input")
        await ctx.send(f"Verifying Permissions for `{ctx.author.id}`...")
        if str(ctx.author.id) not in whitelisted:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
    except Exception as e:
        output = f"**An error has occurred**! Exception: ``{e}``"

        if str(e).startswith("01 "):
            output += "\n***🔴🔴This incident will be reported!🔴🔴***"
        elif str(e).startswith("00 "):
            output += "\n*This incident will **NOT** be reported!*"
        await ctx.send(output)

    else:
        try:
            await env_adj(option, str(msg.content))
        except Exception as e:
            output = f"**An error has occurred**! Exception: ``{e}``"
            print(e)
            await ctx.send(output)
        else:
            await ctx.send("Success!")


@slash.slash(name="set", description="Execute `set` command", guild_ids=guild_ids, )
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
