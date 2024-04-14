from os import listdir

import discord
from discord.ext import commands

from Config import Config


Intents = discord.Intents.default()
Intents.message_content = True
Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)


@Bot.event
async def on_ready():
  for file in listdir("cogs/"):
    if file.endswith(".py"):
      await Bot.load_extension(f"cogs.{file[:-3]}")


Bot.run(Config.Bot["Discord Token"])