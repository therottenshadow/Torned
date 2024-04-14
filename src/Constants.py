from importlib.resources import files
import resources

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
  AHelpIcon = "attachment://HelpIcon.png"
  AInfoIcon = "attachment://InfoIcon.png"
  def ShieldCheck(self):
    return File(files(resources).joinpath("ShieldCheck.png"),filename="ShieldCheck.png")
  def ShieldCross(self):
    return File(files(resources).joinpath("ShieldCross.png"),filename="ShieldCross.png")
  def GreenShieldCheck(self):
    return File(files(resources).joinpath("GreenShieldCheck.png"),filename="GreenShieldCheck.png")
  def RedCross(self):
    return File(files(resources).joinpath("RedCross.png"),filename="RedCross.png")
  def SearchIcon(self):
    return File(files(resources).joinpath("SearchIcon.png"),filename="SearchIcon.png")
  def PriceIcon(self):
    return File(files(resources).joinpath("PriceIcon.png"),filename="PriceIcon.png")
  def PointsIcon(self):
    return File(files(resources).joinpath("PointsIcon.png"),filename="PointsIcon.png")
  def TornedIcon(self):
    return File(files(resources).joinpath("Torned.png"),filename="Torned.png")
  def HelpIcon(self):
    return File(files(resources).joinpath("HelpIcon.png"),filename="HelpIcon.png")
  def InfoIcon(self):
    return File(files(resources).joinpath("InfoIcon.png"),filename="InfoIcon.png")


Images = ImagesObj()
