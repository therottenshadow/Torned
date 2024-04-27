from discord import Role
from discord.ext import commands, tasks

from Classes import ItemDb
from Database import Db
from Config import Config


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

  async def VerifyDiscordName(self, MemberObj, Query):
    if not(Config.Modules["Name Enforcing"]):
      return
    TornNameTemp = f'{Query.TornName} [{Query.TornUserId}]'
    if MemberObj.nick != TornNameTemp:
      print(f"Changing {MemberObj.id} 's nickname from {MemberObj.nick} to {TornNameTemp}")
      await MemberObj.edit(nick=TornNameTemp,reason="Member was not using his Torn Username and ID as Nick")

  async def VerifyRoles(self,MemberObj,GuildObj):
    if not(Config.Modules["User Management"]):
      return
    Query = Db.SearchByDisId(MemberObj.id)
    for UserRole in MemberObj.roles:
      for FIDRole in Config.UserMan["Faction ID to Discord Role"]:
        if UserRole.id == FIDRole["Role"]:
          if FIDRole["Faction ID"] == Query.TornFactionId:
            pass
          else:
            await MemberObj.remove_roles(UserRole,reason="Member no longer meets role criteria")
      for FPosRole in Config.UserMan["Faction Position to Discord Role"]:
        if UserRole.id == FPosRole["Role"]:
          if FPosRole["Position"] == Query.TornFactionPos:
            pass
          else:
            await MemberObj.remove_roles(UserRole,reason="Member no longer meets role criteria")
    for FIDRole in Config.UserMan["Faction ID to Discord Role"]:
      if FIDRole["Faction ID"] == Query.TornFactionId and FIDRole["Role"] not in [x.id for x in MemberObj.roles]:
        await MemberObj.add_roles(GuildObj.get_role(FIDRole["Role"]),reason="Member meets role criteria")
    for FPosRole in Config.UserMan["Faction Position to Discord Role"]:
      if FPosRole["Position"] == Query.TornFactionPos and FPosRole["Role"] not in [x.id for x in MemberObj.roles]:
        await MemberObj.add_roles(GuildObj.get_role(FPosRole["Role"]),reason="Member meets role criteria")
    await self.VerifyDiscordName(MemberObj,Query)

  @tasks.loop(hours=1)
  async def UpdateUsers(self):
    Db.UpdateAllUsers()
    GuildInst = self.bot.get_guild(Config.Bot["Server ID"])
    Query = Db.ReturnAllUsers()
    for User in Query:
      DisMember = GuildInst.get_member(User.DiscordUserId)
      await self.VerifyRoles(DisMember,GuildInst)


async def setup(bot):
  await bot.add_cog(BackgroundCog(bot))