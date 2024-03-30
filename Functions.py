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
  "coverage":"Coverage"
}

def SearchResultEmbedConstructor(ResultList):
  ResultingEmbed = {"Message":"","ImageUrl":""}
  for Result in ResultList:
    for ResultId in Result:
      for x in Result[ResultId]:
        if x == "image" and ResultingEmbed["ImageUrl"] == "":
          ResultingEmbed["ImageUrl"] = Result[ResultId][x]
        elif x == "image" and not(ResultingEmbed["ImageUrl"] == ""):
          pass
        elif x == "name":
          ResultingEmbed["Message"] += f'**{Result[ResultId][x]}**\n'
        elif not((Result[ResultId][x] is None) or (Result[ResultId][x] == "")):
          ResultingEmbed["Message"] += f'**{ApiTranslate[x]}**: {Result[ResultId][x]}\n'
      ResultingEmbed["Message"] += "\n"
  return ResultingEmbed