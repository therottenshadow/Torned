import re
from TornAPIWrapper import TornApiWrapper
from Classes import SanitizeError
from Constants import ApiTranslate

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

def PriceAverageCalculator(PolledItem:dict):
  Result = {"BazaarAverage":0,"LowestBazaar":0,"BazaarAmount":0,"IMarketAverage":0,"LowestIMarket":0,"IMarketAmount":0}
  BazaarCount = 0
  IMarketCount = 0
  if not(PolledItem["bazaar"] is None):
    PolledBazaar = PolledItem["bazaar"][:5]
    for x in PolledBazaar:
      BazaarCount += x["cost"]
      Result["BazaarAmount"] += x["quantity"]
    Result["BazaarAverage"] = BazaarCount/len(PolledBazaar)
    Result["LowestBazaar"] = PolledBazaar[0]["cost"]
  if not(PolledItem["itemmarket"] is None):
    PolledIMarket = PolledItem["itemmarket"][:5]
    for x in PolledIMarket:
      IMarketCount += x["cost"]
      Result["IMarketAmount"] += x["quantity"]
    Result["IMarketAverage"] = IMarketCount/len(PolledIMarket)
    Result["LowestIMarket"] = PolledIMarket[0]["cost"]
  return Result

def PriceEmbedConstructor(ItemName,ItemId,ResultsDict):
  return f"Showing statistics of the first 5 orders in Bazaars and Item Market for **{ItemName}**\n**ID**: {ItemId}\n\n**Item Market**  ({ResultsDict['IMarketAmount']} Items counted)\n`•` Lowest: `${ResultsDict['LowestIMarket']}`\n`•` Average: `${ResultsDict['IMarketAverage']}`\n**Bazaar**  ({ResultsDict['BazaarAmount']} Items counted)\n`•` Lowest: `${ResultsDict['LowestBazaar']}`\n`•` Average: `${ResultsDict['BazaarAverage']}`\n\nPlease remember this is not an accurate reading due to market fluctuations, people buying out orders and lower than average orders"

def SanitizeTornKey(DirtyString: str):
  if len(DirtyString) == 0:
    raise SanitizeError("NullString")
  if len(DirtyString) != 16:
    raise SanitizeError("IncorrectLength")
  elif bool(re.search("[^A-Za-z0-9]",DirtyString)):
    raise SanitizeError("IllegalCharacters")
  else:
    try:
      TornObject = TornApiWrapper(api_key=DirtyString)
      ApiData = TornObject.get_torn(selections=["timestamp"])
      del TornObject
      del ApiData
    except:
      raise SanitizeError("InvalidKey")

def SanitizeSearchTerm(DirtyString: str):
  if bool(re.search("[^A-Za-z0-9-:&/+,!?'’ ]",DirtyString)):
    raise SanitizeError("IllegalCharacters")