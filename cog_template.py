from discord.ext import commands

class My_Cog(commands.Cog, name='Your Cog Name'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='test' , brief='This is the brief description', description='This is the full description')
  async def test(ctx):
    await ctx.send('test')

async def setup(bot):
  await bot.add_cog(My_Cog(bot))