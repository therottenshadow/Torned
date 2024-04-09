import discord
from discord.ext import commands
import Functions
import Classes
from unidecode import unidecode
from Config import Config
from Constants import Images
from Database import Db,User
from TornAPIWrapper import TornApiWrapper

ItemDb = Classes.ItemList(Config.Torn["Torn API Key"])
Intents = discord.Intents.default()
Intents.message_content = True
Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)

@Bot.command()
async def search(ctx,*,SearchString:str=None):
  if SearchString is None:
    await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Item Search**",description="It seems like you haven't given me any search parameters, wanna try that again?").set_thumbnail(url="attachment://RedCross.png"))
    return
  SearchString = unidecode(SearchString)
  try:
    Functions.SanitizeSearchTerm(SearchString)
  except Classes.SanitizeError as Error:
    if 'IllegalCharacters' in str(Error):
      await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="Your search contains illegal characters",description="Your input contains characters that are not allowed because they aren't part of any item's name").set_thumbnail(url="attachment://RedCross.png"))
      return
  if SearchString.isdigit():
    try:
      Embed = Functions.SearchResultEmbedConstructor([ItemDb.SearchById(SearchString)])
      await ctx.reply(embed=discord.Embed(title="**Item Search**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    except KeyError:
      await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Item Search**",description="It seems like this item ID does not exist.").set_thumbnail(url="attachment://RedCross.png"))
  else:
    if len(SearchString) > 2:
      SearchResult = ItemDb.SearchByString(SearchString)
      if len(SearchResult) == 0:
        await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="Seems like your search didn't bring up anything",description="Are you sure what you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence.").set_thumbnail(url="attachment://RedCross.png"))
      else:
        Embed = Functions.SearchResultEmbedConstructor(SearchResult[:3])
        await ctx.reply(embed=discord.Embed(title="**Item Search**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    else:
      await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="Your search term is too short",description="I am not going to look through all that could turn up in that search.").set_thumbnail(url="attachment://RedCross.png"))

@Bot.command()
async def verify(ctx,ApiKey:str=None):
  AuthorId = ctx.message.author.id
  if ApiKey is None:
    DisUser = await Bot.fetch_user(AuthorId)
    channel = await Bot.create_dm(DisUser)
    await channel.send(file=Images.ShieldCheck(),embed=discord.Embed(title="**Verification Procedure**",description="Hi,\n\nto complete the verification procedure please invoke the verify command in this DM and add a **public access** Torn API key, this key is viewable to the server owner, it is not needed to use any higher access key.\n\nTo create an API key, you need to go to your settings page in Torn, and under API Keys you will be able to create one, otherwise, you can use [this handy link](https://www.torn.com/preferences.php#tab=api?&step=addNewKey&title=TornedDiscordBot&type=1)\n\nHere is an example on how to invoke the command\n\n`/verify a1b2c3d4e5f6g7h8`").set_thumbnail(url="attachment://ShieldCheck.png"))
    return
  try:
    Functions.SanitizeTornKey(ApiKey)
  except Classes.SanitizeError:
    await ctx.reply(file=Images.ShieldCross(),embed=discord.Embed(title="**Verification Failed**",description="Please check that the API key you entered is a valid key, it should only contain numbers and letters and be 16 characters in length").set_thumbnail(url="attachment://ShieldCross.png"))
    return
  Query = Db.SearchByDisId(AuthorId)
  if Query is None:
    pass
  elif Query.TornApiKey == "":
    pass
  else:
    await ctx.reply(file=Images.ShieldCross(),embed=discord.Embed(title="**Verification Failed**",description="You are already registered on our database, you have no need to re-register").set_thumbnail(url="attachment://ShieldCross.png"))
    return
  InvokingUser = User(DiscordUserId=AuthorId,TornApiKey=ApiKey)
  InvokingUser.Populate()
  Db.AddAndCommit(InvokingUser)
  del InvokingUser
  await ctx.reply(file=Images.GreenShieldCheck(),embed=discord.Embed(title="**Verification Successful**",description="You have been successfully verified on our database, now you should have been assigned appropiate roles and be able to use all of my services").set_thumbnail(url="attachment://GreenShieldCheck.png"))

@Bot.command()
async def price(ctx,*,SearchString:str=None):
  if SearchString is None:
    await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Price Check**",description="Please introduce the name or ID number of an item to get it's average item market and bazaar prices.\n\nBelow is an example\n`/price Hammer`").set_thumbnail(url="attachment://RedCross.png"))
    return
  SearchString = unidecode(SearchString).lower()
  try:
    Functions.SanitizeSearchTerm(SearchString)
  except Classes.SanitizeError as Error:
    if 'IllegalCharacters' in str(Error):
      await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="Your search contains illegal characters",description="Your input contains characters that are not allowed because they aren't part of any item's name").set_thumbnail(url="attachment://RedCross.png"))
      return
  AuthorId = ctx.message.author.id
  Query = Db.SearchByDisId(AuthorId)
  if Query is None:
    await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Unverified User**",description="It looks like you haven't yet verified, please run /verify to setup an API key with which you can perform a price check").set_thumbnail(url="attachment://RedCross.png"))
    return
  else:
    TornApi = TornApiWrapper(api_key=Query.TornApiKey)
  if SearchString.isdigit():
    DataQuery = TornApi.get_market(SearchString,selections=["bazaar","itemmarket"])
    try:
      InfoQuery = ItemDb.SearchById(SearchString)
    except KeyError:
      await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Price Check**",description="It seems like this item ID does not exist.").set_thumbnail(url="attachment://RedCross.png"))
      return
    Results = Functions.PriceAverageCalculator(DataQuery)
    await ctx.reply(embed=discord.Embed(title="**Price Check Results**",description=f"**{InfoQuery[[x for x in InfoQuery][0]]['name']}**\n**ID**: {[x for x in InfoQuery][0]}\n**Lowest Item Market Price**: {Results['LowestIMarket']}\n**Average Item Market Price**: {Results['IMarketAverage']}\n**Lowest Bazaar Price**: {Results['LowestBazaar']}\n**Average Bazaar Price**: {Results['BazaarAverage']}").set_thumbnail(url=InfoQuery[[x for x in InfoQuery][0]]["image"]))
    return
  else:
    if len(SearchString) > 2:
      SearchResult = ItemDb.SearchByString(SearchString)[:1]
      if len(SearchResult) == 0:
        await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Price Check**",description="Are you sure the item you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence.").set_thumbnail(url="attachment://RedCross.png"))
      else:
        SearchItemId = [x for x in SearchResult[0]][0]
        DataQuery = TornApi.get_market(SearchItemId,selections=["bazaar","itemmarket"])
        Results = Functions.PriceAverageCalculator(DataQuery)
        await ctx.reply(embed=discord.Embed(title="**Price Check Results**",description=f"**{SearchResult[0][SearchItemId]['name']}**\n**ID**: {SearchItemId}\n**Lowest Item Market Price**: {Results['LowestIMarket']}\n**Average Item Market Price**: {Results['IMarketAverage']}\n**Lowest Bazaar Price**: {Results['LowestBazaar']}\n**Average Bazaar Price**: {Results['BazaarAverage']}").set_thumbnail(url=SearchResult[0][SearchItemId]["image"]))
    else:
      await ctx.reply(file=Images.RedCross(),embed=discord.Embed(title="**Price Check**",description="Sorry, but the term you gave me is too undescriptive and is unlikely to return the wanted item's price, please enter at least 3 characters, or even better, the item's ID number").set_thumbnail(url="attachment://RedCross.png"))

@Bot.command()
async def ping(ctx):
  await ctx.reply('pong!')

Bot.run(Config.Bot["Discord Token"])