import re
import inspect
from typing import NoReturn

from TornAPIWrapper import TornApiWrapper
from unidecode import unidecode

from Classes import SanitizeError
from Constants import ApiTranslate
from Config import Config
from Database import Db

def SearchResultEmbedConstructor(ResultList: list) -> dict:
  ResultingEmbed = {"Message":"","ImageUrl":""}
  for Result in ResultList:
    for ResultId in Result:
      for x in Result[ResultId]:
        if x == "image" and ResultingEmbed["ImageUrl"] == "":
          ResultingEmbed["ImageUrl"] = Result[ResultId][x]
        elif x == "image" and not(ResultingEmbed["ImageUrl"] == ""):
          pass
        elif x == "name":
          ResultingEmbed["Message"] += f"**{Result[ResultId][x]}**\n**Item ID**: {ResultId}\n"
        elif x == "coverage":
          ResultingEmbed["Message"] += inspect.cleandoc(
            f"""**Coverage**:
            ⠀⠀**Full Body Coverage**: {Result[ResultId][x]["Full Body Coverage"]}

            ⠀⠀**Head Coverage**: {Result[ResultId][x]["Head Coverage"]}
            ⠀⠀**Throat Coverage**: {Result[ResultId][x]["Throat Coverage"]}
            ⠀⠀**Heart Coverage**: {Result[ResultId][x]["Heart Coverage"]}

            ⠀⠀**Chest Coverage**: {Result[ResultId][x]["Chest Coverage"]}
            ⠀⠀**Stomach Coverage**: {Result[ResultId][x]["Stomach Coverage"]}
            ⠀⠀**Groin Coverage**: {Result[ResultId][x]["Groin Coverage"]}

            ⠀⠀**Arm Coverage**: {Result[ResultId][x]["Arm Coverage"]}
            ⠀⠀**Hand Coverage**: {Result[ResultId][x]["Hand Coverage"]}
            ⠀⠀**Leg Coverage**: {Result[ResultId][x]["Leg Coverage"]}
            ⠀⠀**Foot Coverage**: {Result[ResultId][x]["Foot Coverage"]}
            """)
        elif (Result[ResultId][x] is not None) or (Result[ResultId][x] == ""):
          if isinstance(Result[ResultId][x],int):
            ResultingEmbed["Message"] += f"**{ApiTranslate[x]}**: `{Result[ResultId][x]:,.0f}`\n"
          else:
            ResultingEmbed["Message"] += f"**{ApiTranslate[x]}**: {Result[ResultId][x]}\n"
      ResultingEmbed["Message"] += "\n"
  return ResultingEmbed

def PriceAverageCalculator(PolledItem: dict) -> dict:
  # B=Bazaar IM=Item Market A=Average L=Lowest H=Highest C=Count OI=Order Items
  Result = {"BA":0,"BL":0,"BH":0,"BC":0,"BLOI":0,"IMA":0,"IML":0,"IMH":0,"IMC":0}
  BazaarCount = 0
  IMarketCount = 0
  if PolledItem["bazaar"] is not None:
    PolledBazaar = PolledItem["bazaar"][:5]
    for x in PolledBazaar:
      BazaarCount += x["cost"]
      Result["BC"] += x["quantity"]
    Result["BA"] = BazaarCount/len(PolledBazaar)
    Result["BH"] = PolledBazaar[-1]["cost"]
    Result["BL"] = PolledBazaar[0]["cost"]
    Result["BLOI"] = PolledBazaar[0]["quantity"]
  if PolledItem["itemmarket"] is not None:
    PolledIMarket = PolledItem["itemmarket"][:5]
    for x in PolledIMarket:
      IMarketCount += x["cost"]
      Result["IMC"] += x["quantity"]
    Result["IMA"] = IMarketCount/len(PolledIMarket)
    Result["IMH"] = PolledIMarket[-1]["cost"]
    Result["IML"] = PolledIMarket[0]["cost"]
  return Result

def PriceEmbedConstructor(ItemName: str, ItemId: str, ResultsDict: dict) -> str:
  return inspect.cleandoc(
    f"""Showing statistics of the first 5 orders in Bazaars and Item Market for **{ItemName}**
    **ID**: {ItemId}

    **Item Market**  ({ResultsDict["IMC"]} Items counted)
    • Lowest: `${ResultsDict["IML"]:,.0f}`
    • Average: `${ResultsDict["IMA"]:,.2f}`
    • Highest: `${ResultsDict["IMH"]:,.0f}`
    **Bazaar**  ({ResultsDict["BC"]} Items counted)
    • Lowest: `${ResultsDict["BL"]:,.0f}` - `{ResultsDict["BLOI"]} Items in the order`
    • Average: `${ResultsDict["BA"]:,.2f}`
    • Highest: `${ResultsDict["BH"]:,.0f}`

    You can access the Item Market Page of this item by [clicking here.](https://www.torn.com/imarket.php#/p=shop&step=shop&type=&searchname={ItemId})

    Please remember this is not an accurate reading due to market fluctuations, people buying out orders and lower than average orders
    """)

def SanitizeTornKey(DirtyString: str) -> str:
  DirtyString = unidecode(DirtyString)
  if len(DirtyString) == 0:
    raise SanitizeError("NullString")
  if len(DirtyString) != 16:
    raise SanitizeError("IncorrectLength")
  elif bool(re.search("[^A-Za-z0-9]", DirtyString)):
    raise SanitizeError("IllegalCharacters")
  else:
    try:
      TornObject = TornApiWrapper(api_key=DirtyString)
      ApiData = TornObject.get_torn(selections=["timestamp"])
    except:
      raise SanitizeError("InvalidKey")
  return DirtyString

def SanitizeSearchTerm(DirtyString: str) -> str:
  DirtyString = unidecode(DirtyString).lower()
  if bool(re.search("[^A-Za-z0-9-:&/+,!?'’ ]", DirtyString)):
    raise SanitizeError("IllegalCharacters")
  return DirtyString

def SanitizeDiscordNick(DirtyString: str) -> str:
  if len(DirtyString) > 20:
    raise SanitizeError("NickTooLong")
  return DirtyString

async def VerifyDiscordName(MemberObj, Query):
  if not(Config.Modules["Name Enforcing"]):
    return
  if Query.DiscordNick != "":
    TornNameTemp = f'{Query.DiscordNick} [{Query.TornUserId}]'
  else: TornNameTemp = f'{Query.TornName} [{Query.TornUserId}]'
  if Query.TornApiKey == "" and Query.TornName == "":
    if Query.DiscordNick != "":
      await MemberObj.edit(nick=Query.DiscordNick, reason="Change Member's nick to their chosen nick (no Torn verification)")
    else:
      print(f"Removing {MemberObj.id} 's nickname")
      await MemberObj.edit(nick="", reason="Remove Member's nick")
  elif MemberObj.nick != TornNameTemp:
    print(f"Changing {MemberObj.id} 's nickname from {MemberObj.nick} to {TornNameTemp}")
    await MemberObj.edit(nick=TornNameTemp, reason="Member was not using his Torn Username or chosen nick and ID as Discord nick")

async def VerifyRoles(MemberObj, GuildObj):
  if not(Config.Modules["User Management"]):
    return
  Query = Db.SearchByDisId(MemberObj.id)
  for UserRole in MemberObj.roles:
    for FIDRole in Config.UserMan["Faction ID to Discord Role"]:
      if UserRole.id == FIDRole["Role"]:
        if FIDRole["Faction ID"] == Query.TornFactionId:
          pass
        else:
          await MemberObj.remove_roles(UserRole, reason="Member no longer meets role criteria")
    for FPosRole in Config.UserMan["Faction Position to Discord Role"]:
      if UserRole.id == FPosRole["Role"]:
        if FPosRole["Position"] == Query.TornFactionPos:
          pass
        else:
          await MemberObj.remove_roles(UserRole,reason="Member no longer meets role criteria")
  for FIDRole in Config.UserMan["Faction ID to Discord Role"]:
    if FIDRole["Faction ID"] == Query.TornFactionId and FIDRole["Role"] not in [x.id for x in MemberObj.roles]:
      await MemberObj.add_roles(
        GuildObj.get_role(FIDRole["Role"]),
        reason="Member meets role criteria")
  for FPosRole in Config.UserMan["Faction Position to Discord Role"]:
    if FPosRole["Position"] == Query.TornFactionPos and FPosRole["Role"] not in [x.id for x in MemberObj.roles]:
      await MemberObj.add_roles(
        GuildObj.get_role(FPosRole["Role"]),
        reason="Member meets role criteria")