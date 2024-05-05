from discord import Embed
from discord.ext import commands

from Constants import Images


class My_Cog(commands.Cog, name='Your Cog Name'):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.reply(
        files=[Images.RedCross(),Images.TornedIcon()],
        embed=Embed(description="Looks like you don't have enough permissions to use this command or you aren't in the same server as this bot")
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Permissions Fail",icon_url=Images.ATornedIcon))
    else: raise error

  #@commands.Cog.listener()
  #async def on_command_error(ctx, error):
    #match error:
      #case commands.NoPrivateMessage():
        #await ctx.reply(embed=Embed(
          #files=[],
          #description="")
        #.set_thumbnail(url=Images.ARedCross)
        #.set_author(name="",icon_url=""))
      #case _:
        #raise error

async def setup(bot):
  await bot.add_cog(My_Cog(bot))
