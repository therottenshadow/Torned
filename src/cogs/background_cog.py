"""Cog file for functions running in the background constantly"""

from discord import Role
from discord.ext import commands, tasks

from Classes import ItemDb
from Database import Db
from Config import Config
from Functions import VerifyDiscordName, VerifyRoles

class BackgroundCog(commands.Cog, name='Background Tasks'):
  def __init__(self, bot):
    self.bot = bot
    self.UpdateItemDb.start()
    self.UpdateUsers.start()

  def cog_unload(self):
    self.UpdateItemDb.cancel()
    self.UpdateUsers.cancel()

  @tasks.loop(hours=12)
  async def UpdateItemDb(self):
    ItemDb.UpdateItemList()

  @tasks.loop(hours=1)
  async def UpdateUsers(self):
    Db.UpdateAllUsers()
    GuildInst = self.bot.get_guild(Config.Bot["Server ID"])
    Query = Db.ReturnAllUsers()
    for User in Query:
      DisMember = GuildInst.get_member(User.DiscordUserId)
      await VerifyRoles(DisMember, GuildInst)
      await VerifyDiscordName(DisMember, User)


async def setup(bot):
  await bot.add_cog(BackgroundCog(bot))
