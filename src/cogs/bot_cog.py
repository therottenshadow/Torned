from typing import NoReturn

from discord.ext import commands

class BotCog(commands.Cog, name='Bot'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ping(self, ctx) -> NoReturn:
    await ctx.reply("Pong!")

async def setup(bot):
  await bot.add_cog(BotCog(bot))