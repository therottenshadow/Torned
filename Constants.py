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
  AShieldCheck = "attachment://ShieldCheck.png"
  AShieldCross = "attachment://ShieldCross.png"
  AGreenShieldCheck = "attachment://GreenShieldCheck.png"
  ARedCross = "attachment://RedCross.png"
  ASearchIcon = "attachment://SearchIcon.png"
  APriceIcon = "attachment://PriceIcon.png"
  APointsIcon = "attachment://PointsIcon.png"
  ATornedIcon = "attachment://Torned.png"
  def ShieldCheck(self):
    return File("./resources/ShieldCheck.png",filename="ShieldCheck.png")
  def ShieldCross(self):
    return File("./resources/ShieldCross.png",filename="ShieldCross.png")
  def GreenShieldCheck(self):
    return File("./resources/GreenShieldCheck.png",filename="GreenShieldCheck.png")
  def RedCross(self):
    return File("./resources/RedCross.png",filename="RedCross.png")
  def SearchIcon(self):
    return File("./resources/SearchIcon.png",filename="SearchIcon.png")
  def PriceIcon(self):
    return File("./resources/PriceIcon.png",filename="PriceIcon.png")
  def PointsIcon(self):
    return File("./resources/PointsIcon.png",filename="PointsIcon.png")
  def TornedIcon(self):
    return File("./resources/Torned.png",filename="Torned.png")


Images = ImagesObj()
