import re
from TornAPIWrapper import TornApiWrapper

ApiTranslate = {
  "name":"Name",
  "description":"Description",
  "effect":"Effect",
  "requirement":"Requirement",
  "type":"Type",
  "weapon_type":"Weapon Type",
  "buy_price":"Buy Price",
  "sell_price":"Sell Price",
  "market_value":"Market Value",
  "circulation":"Circulation",
}

def SearchResultEmbedConstructor(ResultList: list):
  ResultingEmbed = {"Message":"","ImageUrl":""}
  for Result in ResultList:
    for ResultId in Result:
      for x in Result[ResultId]:
        if x == "image" and ResultingEmbed["ImageUrl"] == "":
          ResultingEmbed["ImageUrl"] = Result[ResultId][x]
        elif x == "image" and not(ResultingEmbed["ImageUrl"] == ""):
          pass
        elif x == "name":
          ResultingEmbed["Message"] += f'**{Result[ResultId][x]}**\n**Item ID**: {ResultId}\n'
        elif x == "coverage":
          ResultingEmbed["Message"] += f'**Coverage**:\n⠀⠀**Full Body Coverage**: {Result[ResultId][x]["Full Body Coverage"]}\n\n⠀⠀**Head Coverage**: {Result[ResultId][x]["Head Coverage"]}\n⠀⠀**Throat Coverage**: {Result[ResultId][x]["Throat Coverage"]}\n⠀⠀**Heart Coverage**: {Result[ResultId][x]["Heart Coverage"]}\n\n⠀⠀**Chest Coverage**: {Result[ResultId][x]["Chest Coverage"]}\n⠀⠀**Stomach Coverage**: {Result[ResultId][x]["Stomach Coverage"]}\n⠀⠀**Groin Coverage**: {Result[ResultId][x]["Groin Coverage"]}\n\n⠀⠀**Arm Coverage**: {Result[ResultId][x]["Arm Coverage"]}\n⠀⠀**Hand Coverage**: {Result[ResultId][x]["Hand Coverage"]}\n⠀⠀**Leg Coverage**: {Result[ResultId][x]["Leg Coverage"]}\n⠀⠀**Foot Coverage**: {Result[ResultId][x]["Foot Coverage"]}'
        elif not((Result[ResultId][x] is None) or (Result[ResultId][x] == "")):
          ResultingEmbed["Message"] += f'**{ApiTranslate[x]}**: {Result[ResultId][x]}\n'
      ResultingEmbed["Message"] += "\n"
  return ResultingEmbed


def SanitizeTornKey(DirtyString: str):
  KeyRE = re.compile('[^A-Za-z0-9]')
  if not(len(DirtyString) == 16):
    raise ValueError("IncorrectLength")
  elif KeyRE.match(DirtyString):
    raise ValueError("IllegalCharacters")
  else:
    try:
      TornObject = TornApiWrapper(api_key=DirtyString)
      ApiData = TornObject.get_torn(selections=["timestamp"])
      del TornObject
      del ApiData
    except:
      raise ValueError("InvalidKey")

def SanitizeSearchTerm(DirtyString: str):
  SearchTermRE = re.compile("[^A-Za-z0-9-:&/+,!?'’ ]")
  if SearchTermRE.match(DirtyString):
    raise ValueError("IllegalCharacters")