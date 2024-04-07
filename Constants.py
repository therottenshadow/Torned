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
    return File("./resources/ShieldCheck.png", "ShieldCheck.png")
  def ShieldCross(self):
    return File("./resources/ShieldCross.png", "ShieldCross.png")
  def GreenShieldCheck(self):
    return File("./resources/GreenShieldCheck.png", "GreenShieldCheck.png")

Images = ImagesObj()