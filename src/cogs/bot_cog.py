"""Cog file for commands concerning the bot itself"""

from typing import NoReturn

from discord.ext import commands

class BotCog(commands.Cog, name='Bot'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    aliases=["Ping"],
    description="Ping!........Pong!.......This is just a fun command")
  async def ping(self, ctx) -> NoReturn:
    await ctx.reply("Pong!")

async def setup(bot):
  await bot.add_cog(BotCog(bot))
