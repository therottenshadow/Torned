from os import listdir

import discord
from discord.ext import commands

from Config import Config

CogsList = [
  "discord_cog",
  "torn_cog",
  "users_cog",
  "bot_cog"
]

def main():
  Intents = discord.Intents.default()
  Intents.message_content = True
  Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)

  @Bot.event
  async def on_ready():
    for Cog in CogsList:
      await Bot.load_extension(f"cogs.{Cog}")

  Bot.run(Config.Bot["Discord Token"])