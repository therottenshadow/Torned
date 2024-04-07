from discord import File

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

class ImagesObj:
  def ShieldCheck(self):
    return File("./resources/ShieldCheck.webp", "ShieldCheck.webp")
  def ShieldCross(self):
    return File("./resources/ShieldCross.webp", "ShieldCross.webp")

Images = ImagesObj()