import os
import sys
from datetime import datetime
import time

import discord
import redis
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from dotenv import dotenv_values

import utils

r = redis.Redis(host=dotenv_values("config.env")["HOSTNAME"], port=dotenv_values("config.env")["PORT"], db=dotenv_values("config.env")["DB"])


WHITELISTED = dotenv_values("config.env")["whitelisted"].split(",")
bot = commands.Bot(command_prefix="redis ")
slash = SlashCommand(bot, override_type=True, sync_commands=True)

GUILD_IDS = [int(dotenv_values("config.env")["guild_id"])]



@slash.slash(name="Reboot", description=f"", guild_ids=GUILD_IDS)
async def _reboot(ctx):
    now = datetime.now()  # current date and time
    result = discord.Embed(
        title='Rebooting',
        description=f'Execution time: {now}\n\n**ATTEMPTING REBOOT**',
        colour=discord.Colour.teal()
    )
    result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=result)
    time.sleep(2)
    try:
        if str(ctx.author.id) not in WHITELISTED:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
        output = "Verification Complete!\nRebooting..."
    except Exception as e:
        output = f"**An error has occurred**! Exception: ``{e}``... *Sorry!*"
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


@slash.slash(name="config", description="Edit `config.env` file", guild_ids=GUILD_IDS, options=[
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


    try:
        if option == "DB":
            await ctx.send(f"Select new database index (MUST BE NUMBER)")
            msg = await bot.wait_for("message")
            await ctx.message.delete()
            if not (utils.check_int(msg)):
                raise Exception("00 Invalid Input")
        elif option == "PORT":
            await ctx.send(f"Select new port for Redis-bot (MUST BE NUMBER)")
            msg = await bot.wait_for("message")
            await ctx.message.delete()
            if not (utils.check_int(msg)):
                raise Exception("00 Invalid Input")
        elif option == "HOSTNAME":
            await ctx.send(f"Select new IP Address for Redis-bot (MUST BE VALID IP)")
            msg = await bot.wait_for("message")
            await ctx.message.delete()
            if not (utils.check_ip(msg)):
                raise Exception("00 Invalid Input")
        await ctx.send(f"Verifying Permissions for `{ctx.author.id}`...")
        if str(ctx.author.id) not in WHITELISTED:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
    except Exception as e:
        output = f"**An error has occurred**! Exception: ``{e}``... *Sorry!*"

        if str(e).startswith("01 "):
            output += "\n***🔴🔴This incident will be reported!🔴🔴***"
        elif str(e).startswith("00 "):
            output += "\n*This incident will **NOT** be reported!*"
        await ctx.send(output)

    else:
        try:
            await utils.dotenv_adjustment(option, str(msg.content))
        except Exception as e:
            output = f"**An error has occurred**! Exception: ``{e}``... *Sorry!*"
            print(e)
            await ctx.send(output)
        else:
            await ctx.send("Success!\nA Reboot is required to apply changes to active session")


@slash.slash(name="SET", description="Set value in key", guild_ids=GUILD_IDS, )
async def _set(ctx, key, value):
    now = datetime.now()  # current date and time
    r.set(str(key), str(value))
    true_value = r.get(str(key)).decode("utf-8")
    result = discord.Embed(
        title='SET:',
        description=f'Execution Time: {now}\n\nDatabase: ``{key}``: ``{true_value}``',
        colour=discord.Colour.blue()

    )
    result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=result)


@slash.slash(name="GET", description="Get value in key", guild_ids=GUILD_IDS, )
async def _get(ctx, key):
    now = datetime.now()  # current date and time
    value = r.get(str(key)).decode("utf-8")
    result = discord.Embed(
        title='GET:',
        description=f'Execution Time: {now}\n\n``{key}``: ``{value}``',
        colour=discord.Colour.blue()
    )
    result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=result)


@slash.slash(name="DEL", description="Delete key", guild_ids=GUILD_IDS, )
async def _get(ctx, key):
    try:
        if str(ctx.message.id) not in WHITELISTED:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
        now = datetime.now()  # current date and time
        r.delete(str(key))
        result = discord.Embed(
            title='DEL:',
            description=f'Execution Time: {now}\n\nDeleted Key: ``{key}``',
            colour=discord.Colour.blue()
        )
        result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        await ctx.send(embed=result)
    except Exception as e:
        await ctx.send(f"**An error has occurred**! Exception: ``{e}``... *Sorry!*")


@slash.slash(name="EXPIRE", description="Key will be deleted in 120 seconds", guild_ids=GUILD_IDS, )
async def _get(ctx, key, time):
    now = datetime.now()  # current date and time
    try:
        if str(ctx.message.id) not in WHITELISTED:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
        r.expire(str(key), int(time))
        result = discord.Embed(
            title='EXPIRE:',
            description=f'Execution Time: {now}\n\nDeleted Key: ``{key}``',
            colour=discord.Colour.blue()
        )
        result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        await ctx.send(embed=result)
    except Exception as e:
        await ctx.send(f"**An error has occurred**! Exception: ``{e}``... *Sorry!*")


@slash.slash(name="TTL", description="Returns the number of seconds until a key is deleted", guild_ids=GUILD_IDS)
async def _ttl(ctx, key):
    now = datetime.now()  # current date and time
    try:
        if str(ctx.message.id) not in WHITELISTED:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
        time_left = r.ttl(key)
        result = discord.Embed(
            title='TTL:',
            description=f'Execution Time: {now}\n\nTime Left for {key}: ``{time_left}``',
            colour=discord.Colour.blue()
        )
        result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        await ctx.send(embed=result)
    except Exception as e:
        await ctx.send(f"**An error has occurred**! Exception: ``{e}``... *Sorry!*")


@slash.slash(name="KEYS", description="For Finding all keys", guild_ids=GUILD_IDS)
async def _keys(ctx):
    now = datetime.now()  # current date and time
    try:
        if str(ctx.message.id) not in WHITELISTED:
            raise Exception("01 Permission Denied! User id is not found in whitelisted")
        keys = r.keys()
        result = discord.Embed(
            title='KEYS:',
            description=f'Execution Time: {now}\n\nKeys: {keys}``',
            colour=discord.Colour.blue()
        )
        result.set_footer(text="This is an open source project by @YonLiud at GitHub", icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
        await ctx.send(embed=result)
    except Exception as e:
        await ctx.send(f"**An error has occurred**! Exception: ``{e}``... *Sorry!*")





@bot.event
async def on_ready():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print(f"bot | Launch Time:  ", date_time)
    print(f"Bot | Status:     Operational")
    print(f"Bot | ID:         {format(bot.user.id)}")
    print(f"Bot | Name:       {format(bot.user.name)}")
    print(f"Bot is ready to use")


bot.run(str(dotenv_values("token.env")["TOKEN"]))
