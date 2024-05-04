from importlib.resources import files

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
  FShieldCheck = "ShieldCheck.png"
  FShieldCross = "ShieldCross.png"
  FGreenShieldCheck = "GreenShieldCheck.png"
  FRedCross = "RedCross.png"
  FSearchIcon = "SearchIcon.png"
  FPriceIcon = "PriceIcon.png"
  FPointsIcon = "PointsIcon.png"
  FTorned = "Torned.png"
  FHelpIcon = "HelpIcon.png"
  FInfoIcon = "InfoIcon.png"
  FGreenCheck = "GreenCheck.png"
  AShieldCheck = f"attachment://{self.FShieldCheck}"
  AShieldCross = f"attachment://{self.FShieldCross}"
  AGreenShieldCheck = f"attachment://{self.FGreenShieldCheck}"
  ARedCross = f"attachment://{self.FRedCross}"
  ASearchIcon = f"attachment://{self.FSearchIcon}"
  APriceIcon = f"attachment://{self.FPriceIcon}"
  APointsIcon = f"attachment://{self.FPointsIcon}"
  ATornedIcon = f"attachment://{self.FTorned}"
  AHelpIcon = f"attachment://{self.FHelpIcon}"
  AInfoIcon = f"attachment://{self.FInfoIcon}"
  AGreenCheck = f"attachment://{self.FGreenCheck}"
  def ShieldCheck(self):
    return File(
      files("resources").joinpath(self.FShieldCheck).open("rb"),
      filename=self.FShieldCheck)
  def ShieldCross(self):
    return File(
      files("resources").joinpath(self.FShieldCross).open("rb"),
      filename=self.FShieldCross)
  def GreenShieldCheck(self):
    return File(
      files("resources").joinpath(self.FGreenShieldCheck).open("rb"),
      filename=self.FGreenShieldCheck)
  def RedCross(self):
    return File(
      files("resources").joinpath(self.FRedCross).open("rb"),
      filename=self.FRedCross)
  def SearchIcon(self):
    return File(
      files("resources").joinpath(self.FSearchIcon).open("rb"),
      filename=self.FSearchIcon)
  def PriceIcon(self):
    return File(
      files("resources").joinpath(self.FPriceIcon).open("rb"),
      filename=self.FPriceIcon)
  def PointsIcon(self):
    return File(
      files("resources").joinpath(self.FPointsIcon).open("rb"),
      filename=self.FPointsIcon)
  def TornedIcon(self):
    return File(
      files("resources").joinpath(self.FTorned).open("rb"),
      filename=self.FTorned)
  def HelpIcon(self):
    return File(
      files("resources").joinpath(self.FHelpIcon).open("rb"),
      filename=self.FHelpIcon)
  def InfoIcon(self):
    return File(
      files("resources").joinpath(self.FInfoIcon).open("rb"),
      filename=self.FInfoIcon)
  def GreenCheck(self):
    return File(
      files("resources").joinpath(self.FGreenCheck).open("rb"),
      filename=self.FGreenCheck)


Images = ImagesObj()
