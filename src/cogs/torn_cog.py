"""Cog file for commands that concern pulling data from Torn API"""

import inspect

from discord import Embed
from discord.ext import commands
from TornAPIWrapper import TornApiWrapper

import Color
from Functions import SanitizeSearchTerm, PriceAverageCalculator, PriceEmbedConstructor, SearchResultEmbedConstructor, is_member, is_access_1
from Constants import Images
from Classes import SanitizeError, ItemDb
from Database import Db


class TornCog(commands.Cog, name='Torn'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    aliases=["Search","lookup","Lookup"],
    usage="[Item Name or Item ID Number]",
    description="This command serves to search the list of existing Torn items whether you are unsure about the item's name or you want to double check some information about the item.")
  @commands.check(is_member)
  @commands.check(is_access_1)
  async def search(self, ctx, *, SearchString: str = None) -> None:
    """Search for a Torn item and it's information"""
    if SearchString is None:
      await ctx.reply(
        files=[Images.TornedIcon(),Images.SearchIcon()],
        embed=Embed(
          description=inspect.cleandoc(
            """Hello!,

            This command serves to search the list of existing Torn items whether you are unsure about the item's name or you want to double check some information about the item.

            Here is an example for searching for the Baseball Bat
            `/search Baseball Bat`
            """),
          color=Color.Cyan)
        .set_thumbnail(url=Images.ASearchIcon)
        .set_author(name="Item Search",icon_url=Images.ATornedIcon))
      return
    try:
      SearchString = SanitizeSearchTerm(SearchString)
    except SanitizeError as Error:
      if "IllegalCharacters" in str(Error):
        await ctx.reply(
          files=[Images.RedCross(),Images.SearchIcon()],
          embed=Embed(
            description=inspect.cleandoc(
              """Your search contains illegal characters.

              Your input contains characters that are not allowed because they aren't part of any item's name.
              """),
          color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Item Search",icon_url=Images.ASearchIcon))
        return
    if SearchString.isdigit():
      SearchList = []
      try:
        SearchList.append(ItemDb.SearchById(SearchString))
      except KeyError:
        await ctx.reply(
          files=[Images.RedCross(),Images.SearchIcon()],
          embed=Embed(
            description="It seems like this item ID does not exist.",
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Item Search",icon_url=Images.ASearchIcon))
      else:
        ResultEmbed = SearchResultEmbedConstructor(SearchList)
        await ctx.reply(
          file=Images.SearchIcon(),
          embed=Embed(
            description=ResultEmbed["Message"],
              color=Color.Cyan)
          .set_thumbnail(url=ResultEmbed["ImageUrl"])
          .set_author(name="Item Search Results",icon_url=Images.ASearchIcon))
    else:
      if len(SearchString) > 2:
        SearchResult = ItemDb.SearchByString(SearchString)
        if len(SearchResult) == 0:
          await ctx.reply(
            files=[Images.RedCross(),Images.SearchIcon()],
            embed=Embed(
              description=inspect.cleandoc(
                """Seems like your search didn't bring up anything.

                Are you sure what you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence.
                """),
              color=Color.Red)
            .set_thumbnail(url=Images.ARedCross)
            .set_author(name="Item Search",icon_url=Images.ASearchIcon))
        else:
          ResultEmbed = SearchResultEmbedConstructor(SearchResult[:3])
          await ctx.reply(
            file=Images.SearchIcon(),
            embed=Embed(
              description=ResultEmbed["Message"],
              color=Color.Cyan)
            .set_thumbnail(url=ResultEmbed["ImageUrl"])
            .set_author(name="Item Search Results",icon_url=Images.ASearchIcon))
      else:
        await ctx.reply(
          files=[Images.RedCross(),Images.SearchIcon()],
          embed=Embed(
            description=inspect.cleandoc(
              """Your search term is too short.

              I am not going to look through all that could turn up in that search.
              """),
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Item Search",icon_url=Images.ASearchIcon))

  @commands.command(
    aliases=["Price"],
    usage="[Item Name or Item ID Number]",
    description="This command allows you to get the price of the lowest sell order, average of 5 sell orders and highest sell order for an item on the item market or bazaar. This command needs you to have completed the verification process by using /verify.")
  @commands.check(is_member)
  @commands.check(is_access_1)
  async def price(self, ctx, *, SearchString: str = None) -> None:
    """Get Item market and Bazaar price averages for an item"""
    if SearchString is None:
      await ctx.reply(
        files=[Images.TornedIcon(),Images.PriceIcon()],
        embed=Embed(
          description=inspect.cleandoc(
            """Please introduce the name or ID number of an item to get it's average item market and bazaar prices.

            Below is an example for polling the prices of Hammer.
            `/price Hammer`
            """),
          color=Color.Yellow)
        .set_thumbnail(url=Images.APriceIcon)
        .set_author(name="Price Check",icon_url=Images.ATornedIcon))
      return
    try:
      SearchString = SanitizeSearchTerm(SearchString)
    except SanitizeError as Error:
      if "IllegalCharacters" in str(Error):
        await ctx.reply(
          files=[Images.RedCross(),Images.PriceIcon()],
          embed=Embed(
            description=inspect.cleandoc(
              """Your search contains illegal characters.

              Your input contains characters that are not allowed because they aren't part of any item's name
              """),
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Price Check",icon_url=Images.APriceIcon))
        return
    AuthorId = ctx.message.author.id
    Query = Db.SearchByDisId(AuthorId)
    if Query is None:
      await ctx.reply(
        files=[Images.RedCross(),Images.PriceIcon()],
        embed=Embed(
          description="It looks like you haven't yet verified, please run /verify to setup an API key with which you can perform a price check",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Price Check",icon_url=Images.APriceIcon))
      return
    TornApi = TornApiWrapper(api_key=Query.TornApiKey)
    if SearchString.isdigit():
      DataQuery = TornApi.get_market(SearchString,selections=["bazaar","itemmarket"])
      try:
        InfoQuery = ItemDb.SearchById(SearchString)
      except KeyError:
        await ctx.reply(
          files=[Images.RedCross(),Images.PriceIcon()],
          embed=Embed(
            description="It seems like this item ID does not exist.",
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Price Check",icon_url=Images.APriceIcon))
        return
      Results = PriceAverageCalculator(DataQuery)
      Desc = PriceEmbedConstructor(InfoQuery[[x for x in InfoQuery][0]]["name"],[x for x in InfoQuery][0],Results)
      await ctx.reply(
        file=Images.PriceIcon(),
        embed=Embed(
          description=Desc,
          color=Color.Yellow)
        .set_thumbnail(url=InfoQuery[[x for x in InfoQuery][0]]["image"])
        .set_author(name="Price Check Results",icon_url=Images.APriceIcon))
    else:
      if len(SearchString) > 2:
        SearchResult = ItemDb.SearchByString(SearchString)[:1]
        if len(SearchResult) == 0:
          await ctx.reply(
            files=[Images.RedCross(),Images.PriceIcon()],
            embed=Embed(
              description="Are you sure the item you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence.",
              color=Color.Red)
            .set_thumbnail(url=Images.ARedCross)
            .set_author(name="Price Check",icon_url=Images.APriceIcon))
        else:
          SearchItemId = [x for x in SearchResult[0]][0]
          DataQuery = TornApi.get_market(SearchItemId,selections=["bazaar","itemmarket"])
          Results = PriceAverageCalculator(DataQuery)
          Desc = PriceEmbedConstructor(SearchResult[0][SearchItemId]["name"],SearchItemId,Results)
          await ctx.reply(
            file=Images.PriceIcon(),
            embed=Embed(
              description=Desc,
              color=Color.Yellow)
            .set_thumbnail(url=SearchResult[0][SearchItemId]["image"])
            .set_author(name="Price Check Results",icon_url=Images.APriceIcon))
      else:
        await ctx.reply(
          files=[Images.RedCross(),Images.PriceIcon()],
          embed=Embed(
            description="Sorry, but the term you gave me is too undescriptive and is unlikely to return the wanted item's price, please enter at least 3 characters, or even better, the item's ID number",
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Price Check",icon_url=Images.APriceIcon))

  @commands.command(
    aliases=["point","Points","Point"],
    description="This commands allows you to query the first 5 sell orders for points on the points market and get their price per point, quantity and total price. This command needs you to have completed the verification process by using /verify.")
  @commands.check(is_member)
  @commands.check(is_access_1)
  async def points(self, ctx) -> None:
    """Get the information of the first 5 sell orders of points on the point market"""
    AuthorId = ctx.message.author.id
    Query = Db.SearchByDisId(AuthorId)
    if Query is None:
      await ctx.reply(
        files=[Images.RedCross()],
        embed=Embed(
          description="It looks like you haven't yet verified, please run /verify to setup an API key with which you can perform a points price check",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Points Price Check",icon_url=Images.ARedCross))
      return
    else:
      TornApi = TornApiWrapper(api_key=Query.TornApiKey)
    DataDict = TornApi.get_market(0,selections=["pointsmarket"])["pointsmarket"]
    Data = []
    for x in DataDict:
      Data.append(DataDict[x])
    Data = Data[:5]
    Message = "Here is the data of the first 5 sell orders for points:\n\n"
    for x in Data:
      Message += f'• Price/Point: `${x["cost"]:,.0f}` Quantity: `{x["quantity"]}` Total Price: `${x["total_cost"]:,.0f}`\n'
    Message += inspect.cleandoc(
      """[Here is a link to go directly to the Points Market](https://www.torn.com/pmarket.php)

      Please remember this is not an accurate reading of the points market, the volume of sells is so high you might not get to buy these specific orders, this is a mere estimation
      """)
    await ctx.reply(
      files=[Images.PointsIcon(),Images.TornedIcon()],
      embed=Embed(
        description=Message,
        color=Color.Yellow)
      .set_thumbnail(url=Images.APointsIcon)
      .set_author(name="Points Price Check",icon_url=Images.ATornedIcon))

async def setup(bot):
  await bot.add_cog(TornCog(bot))
