"""Cog file for commands that mainly concern Discord stuff"""

from typing import NoReturn
import inspect

from discord import Embed
from discord.ext import commands

from Constants import Images
import Color


class HALP(commands.MinimalHelpCommand):
  async def send_pages(self) -> NoReturn:
    destination = self.get_destination()
    for page in self.paginator.pages:
      await destination.send(
        files=[Images.TornedIcon(),Images.HelpIcon()],
        embed=Embed(
          description=page)
          .set_thumbnail(url=Images.AHelpIcon)
          .set_author(name="Help Command",icon_url=Images.ATornedIcon))


class DiscordCog(commands.Cog, name='Discord'):
  def __init__(self, bot):
    self.bot = bot
    self._original_help_command = bot.help_command
    bot.help_command = HALP()
    bot.help_command.cog = self

  def cog_unload(self):
    self.bot.help_command = self._original_help_command

  @commands.command(
    aliases=["Info","information"],
    description="Shows a description of the bot, how to know more about commands and a link to the GitHub repository")
  async def info(self, ctx) -> NoReturn:
    """Shows information about the code I am running!"""
    await ctx.reply(
      files=[Images.TornedIcon(),Images.InfoIcon()],
      embed=Embed(
        color=Color.LightGrey,
        description=inspect.cleandoc("""
          Hello!, I am a bot running Torned, a simple bot program developed by therottenshadow[3055842] that has been coded in Python to be able to poll info from Torn from outside the game.

          If you want to learn more about my capabilities, you can see all possible commands by running the `/help` command.

          If you want to learn more about my code, you can do so on my [GitHub](https://github.com/therottenshadow/Torned)
          """))
      .set_thumbnail(url=Images.ATornedIcon)
      .set_author(name="Info Command",icon_url=Images.AInfoIcon)
    )


async def setup(bot):
  await bot.add_cog(DiscordCog(bot))
