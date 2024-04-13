import discord
from discord.ext import commands
import Functions
import Classes
from unidecode import unidecode
from Config import Config
from Constants import Images
from Database import Db,User
from TornAPIWrapper import TornApiWrapper
import Color

ItemDb = Classes.ItemList(Config.Torn["Torn API Key"])
Intents = discord.Intents.default()
Intents.message_content = True
Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)

@Bot.command(
  aliases=["lookup","Lookup","Search"])
async def search(ctx,*,SearchString:str=None):
  """Search for a Torn item and it's information"""
  if SearchString is None:
    await ctx.reply(
      files=[Images.RedCross(),Images.SearchIcon()],
      embed=discord.Embed(
        description="It seems like you haven't given me any search parameters, wanna try that again?",
        color=Color.Red)
      .set_thumbnail(url=Images.ARedCross)
      .set_author(name="Item Search",icon_url=Images.ASearchIcon))
    return
  SearchString = unidecode(SearchString)
  try:
    Functions.SanitizeSearchTerm(SearchString)
  except Classes.SanitizeError as Error:
    if 'IllegalCharacters' in str(Error):
      await ctx.reply(
        files=[Images.RedCross(),Images.SearchIcon()],
        embed=discord.Embed(
          description="Your search contains illegal characters.\nYour input contains characters that are not allowed because they aren't part of any item's name",
        color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Item Search",icon_url=Images.ASearchIcon))
      return
  if SearchString.isdigit():
    try:
      Embed = Functions.SearchResultEmbedConstructor([ItemDb.SearchById(SearchString)])
      await ctx.reply(
        file=Images.SearchIcon(),
        embed=discord.Embed(
          description=Embed["Message"],
            color=Color.Cyan)
        .set_thumbnail(url=Embed["ImageUrl"])
        .set_author(name="Item Search Results",icon_url=Images.ASearchIcon))
    except KeyError:
      await ctx.reply(
        files=[Images.RedCross(),Images.SearchIcon()],
        embed=discord.Embed(
          description="It seems like this item ID does not exist.",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Item Search",icon_url=Images.ASearchIcon))
  else:
    if len(SearchString) > 2:
      SearchResult = ItemDb.SearchByString(SearchString)
      if len(SearchResult) == 0:
        await ctx.reply(
          files=[Images.RedCross(),Images.SearchIcon()],
          embed=discord.Embed(
            description="Seems like your search didn't bring up anything.\nAre you sure what you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence.",
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Item Search",icon_url=Images.ASearchIcon))
      else:
        Embed = Functions.SearchResultEmbedConstructor(SearchResult[:3])
        await ctx.reply(
          file=Images.SearchIcon(),
          embed=discord.Embed(
            description=Embed["Message"],
            color=Color.Cyan)
          .set_thumbnail(url=Embed["ImageUrl"])
          .set_author(name="Item Search Results",icon_url=Images.ASearchIcon))
    else:
      await ctx.reply(
        files=[Images.RedCross(),Images.SearchIcon()],
        embed=discord.Embed(
          description="Your search term is too short.\nI am not going to look through all that could turn up in that search.",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Item Search",icon_url=Images.ASearchIcon))

@Bot.command(
  aliases=["Verify"])
async def verify(ctx,ApiKey:str=None):
  """Asociate a Torn API key with your Discord Account"""
  AuthorId = ctx.message.author.id
  if ApiKey is None:
    DisUser = await Bot.fetch_user(AuthorId)
    channel = await Bot.create_dm(DisUser)
    await channel.send(
      file=Images.ShieldCheck(),
      embed=discord.Embed(
        title="**Verification Procedure**",
        description="Hi,\n\nto complete the verification procedure please invoke the verify command in this DM and add a **public access** Torn API key, this key is viewable to the server owner, it is not needed to use any higher access key.\n\nTo create an API key, you need to go to your settings page in Torn, and under API Keys you will be able to create one, otherwise, you can use [this handy link](https://www.torn.com/preferences.php#tab=api?&step=addNewKey&title=TornedDiscordBot&type=1)\n\nHere is an example on how to invoke the command\n\n`/verify a1b2c3d4e5f6g7h8`",
        color=Color.Violet)
      .set_thumbnail(url=Images.AShieldCheck))
    return
  try:
    Functions.SanitizeTornKey(ApiKey)
  except Classes.SanitizeError:
    await ctx.reply(
      file=Images.ShieldCross(),
      embed=discord.Embed(
        title="**Verification Failed**",
        description="Please check that the API key you entered is a valid key, it should only contain numbers and letters and be 16 characters in length",
        color=Color.Red)
      .set_thumbnail(url=Images.AShieldCross))
    return
  Query = Db.SearchByDisId(AuthorId)
  if Query is None:
    pass
  elif Query.TornApiKey == "":
    pass
  else:
    await ctx.reply(
      file=Images.ShieldCross(),
      embed=discord.Embed(
        title="**Verification Failed**",
        description="You are already registered on our database, you have no need to re-register",
        color=Color.Red)
      .set_thumbnail(url=Images.AShieldCross))
    return
  InvokingUser = User(DiscordUserId=AuthorId,TornApiKey=ApiKey)
  InvokingUser.Populate()
  Db.AddAndCommit(InvokingUser)
  del InvokingUser
  await ctx.reply(
    file=Images.GreenShieldCheck(),
    embed=discord.Embed(
      title="**Verification Successful**",
      description="You have been successfully verified on our database, now you should have been assigned appropiate roles and be able to use all of my services",
      color=Color.Green)
    .set_thumbnail(url=Images.AGreenShieldCheck))

@Bot.command(
  aliases=["Price"])
async def price(ctx,*,SearchString:str=None):
  """Get Item market and Bazaar price averages for an item"""
  if SearchString is None:
    await ctx.reply(
      files=[Images.RedCross(),Images.PriceIcon()],
      embed=discord.Embed(
        description="Please introduce the name or ID number of an item to get it's average item market and bazaar prices.\n\nBelow is an example\n`/price Hammer`",
        color=Color.Red)
      .set_thumbnail(url=Images.ARedCross)
      .set_author(name="Price Check",icon_url=Images.APriceIcon))
    return
  SearchString = unidecode(SearchString).lower()
  try:
    Functions.SanitizeSearchTerm(SearchString)
  except Classes.SanitizeError as Error:
    if 'IllegalCharacters' in str(Error):
      await ctx.reply(
        files=[Images.RedCross(),Images.PriceIcon()],
        embed=discord.Embed(
          description="Your search contains illegal characters.\n\nYour input contains characters that are not allowed because they aren't part of any item's name",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Price Check",icon_url=Images.APriceIcon))
      return
  AuthorId = ctx.message.author.id
  Query = Db.SearchByDisId(AuthorId)
  if Query is None:
    await ctx.reply(
      files=[Images.RedCross(),Images.PriceIcon()],
      embed=discord.Embed(
        description="It looks like you haven't yet verified, please run /verify to setup an API key with which you can perform a price check",
        color=Color.Red)
      .set_thumbnail(url=Images.ARedCross)
      .set_author(name="Price Check",icon_url=Images.APriceIcon))
    return
  else:
    TornApi = TornApiWrapper(api_key=Query.TornApiKey)
  if SearchString.isdigit():
    DataQuery = TornApi.get_market(SearchString,selections=["bazaar","itemmarket"])
    try:
      InfoQuery = ItemDb.SearchById(SearchString)
    except KeyError:
      await ctx.reply(
        files=[Images.RedCross(),Images.PriceIcon()],
        embed=discord.Embed(
          description="It seems like this item ID does not exist.",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Price Check",icon_url=Images.APriceIcon))
      return
    Results = Functions.PriceAverageCalculator(DataQuery)
    Desc = Functions.PriceEmbedConstructor(InfoQuery[[x for x in InfoQuery][0]]['name'],[x for x in InfoQuery][0],Results)
    await ctx.reply(
      file=Images.PriceIcon(),
      embed=discord.Embed(
        description=Desc,
        color=Color.Yellow)
      .set_thumbnail(url=InfoQuery[[x for x in InfoQuery][0]]["image"])
      .set_author(name="Price Check Results",icon_url=Images.APriceIcon))
    return
  else:
    if len(SearchString) > 2:
      SearchResult = ItemDb.SearchByString(SearchString)[:1]
      if len(SearchResult) == 0:
        await ctx.reply(
          files=[Images.RedCross(),Images.PriceIcon()],
          embed=discord.Embed(
            description="Are you sure the item you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence.",
            color=Color.Red)
          .set_thumbnail(url=Images.ARedCross)
          .set_author(name="Price Check",icon_url=Images.APriceIcon))
      else:
        SearchItemId = [x for x in SearchResult[0]][0]
        DataQuery = TornApi.get_market(SearchItemId,selections=["bazaar","itemmarket"])
        Results = Functions.PriceAverageCalculator(DataQuery)
        Desc = Functions.PriceEmbedConstructor(SearchResult[0][SearchItemId]['name'],SearchItemId,Results)
        await ctx.reply(
          file=Images.PriceIcon(),
          embed=discord.Embed(
            description=Desc,
            color=Color.Yellow)
          .set_thumbnail(url=SearchResult[0][SearchItemId]["image"])
          .set_author(name="Price Check Results",icon_url=Images.APriceIcon))
    else:
      await ctx.reply(
        files=[Images.RedCross(),Images.PriceIcon()],
        embed=discord.Embed(
          description="Sorry, but the term you gave me is too undescriptive and is unlikely to return the wanted item's price, please enter at least 3 characters, or even better, the item's ID number",
          color=Color.Red)
        .set_thumbnail(url=Images.ARedCross)
        .set_author(name="Price Check",icon_url=Images.APriceIcon))

@Bot.command(
  aliases=["point","Points","Point"])
async def points(ctx):
  """Get the information of the first 5 sell orders of points on the point market"""
  AuthorId = ctx.message.author.id
  Query = Db.SearchByDisId(AuthorId)
  if Query is None:
    await ctx.reply(
      files=[Images.RedCross()],
      embed=discord.Embed(
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
  Message += """
[Here is a link to go directly to the Points Market](https://www.torn.com/pmarket.php)

Please remember this is not an accurate reading of the points market, the volume of sells is so high you might not get to buy these specific orders, this is a mere estimation"""
  await ctx.reply(
    files=[Images.PointsIcon(),Images.TornedIcon()],
    embed=discord.Embed(
      description=Message,
      color=Color.Yellow)
    .set_thumbnail(url=Images.APointsIcon)
    .set_author(name="Points Price Check",icon_url=Images.ATornedIcon))

class HALP(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(
              files=[Images.TornedIcon(),Images.HelpIcon()],
              embed=discord.Embed(
                description=page)
              .set_thumbnail(url=Images.ATornedIcon)
              .set_author(name="Help Command",icon_url=Images.AHelpIcon))
Bot.help_command = HALP()

@Bot.command(
  aliases=["info","information"],
  description="Shows a description of the bot, how to know more about commands and a link to the GitHub repository",)
async def Info(ctx):
  """Shows information about the code I am running!"""
  await ctx.reply(
    files=[Images.TornedIcon(),Images.InfoIcon()],
    embed=discord.Embed(
      color=Color.LightGrey,
      description=
"""Hello!, I am a bot running Torned, a simple bot program developed by therottenshadow[3055842] that has been coded in Python to be able to poll info from Torn from outside the game.

If you want to learn more about my capabilities, you can see all possible commands by running the `/help` command.

If you want to learn more about my code, you can do so on my [GitHub](https://github.com/therottenshadow/Torned)""")
    .set_thumbnail(url=Images.ATornedIcon)
    .set_author(name="Info Command",icon_url=Images.AInfoIcon)
  )

@Bot.command()
async def ping(ctx):
  await ctx.reply('Pong!')

Bot.run(Config.Bot["Discord Token"])