from dotenv import dotenv_values
import redis
import discord

config = dotenv_values("config.env")

client = discord.client()





client.run(dotenv_values("token.env")["TOKEN"])

if __name__ == '__main__':
    print(config)