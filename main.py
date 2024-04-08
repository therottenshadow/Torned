import discord
from discord.ext import commands
import Functions
import Classes
from unidecode import unidecode
from Config import Config
from Constants import Images
from Database import Db,User

ItemDb = Classes.ItemList(Config.Torn["Torn API Key"])
Intents = discord.Intents.default()
Intents.message_content = True
Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)

@Bot.command()
async def search(ctx,*,SearchString:str=None):
  if SearchString is None:
    await ctx.reply(embed=discord.Embed(title="**Item Search**",description="It seems like you haven't given me any search parameters, wanna try that again?"))
    return
  SearchString = unidecode(SearchString)
  try:
    Functions.SanitizeSearchTerm(SearchString)
  except Classes.SanitizeError as Error:
    if 'IllegalCharacters' in str(Error):
      await ctx.reply(embed=discord.Embed(title="Your search contains illegal characters",description="Your input contains characters that are not allowed because they aren't part of any item's name"))
      return
  if SearchString.isdigit():
    try:
      Embed = Functions.SearchResultEmbedConstructor([ItemDb.SearchById(SearchString)])
      await ctx.reply(embed=discord.Embed(title="**Item Search**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    except KeyError:
      await ctx.reply(embed=discord.Embed(title="**Item Search**",description="It seems like this item ID does not exist."))
  else:
    if len(SearchString) >= 3:
      SearchResult = ItemDb.SearchByString(SearchString)
      if len(SearchResult) == 0:
        await ctx.reply(embed=discord.Embed(title="Seems like your search didn't bring up anything",description="Are you sure what you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence."))
      else:
        Embed = Functions.SearchResultEmbedConstructor(SearchResult[:3])
        await ctx.reply(embed=discord.Embed(title="**Item Search**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    else:
      await ctx.reply(embed=discord.Embed(title="Your search term is too short",description="I am not going to look through all that could turn up in that search."))

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
  except Classes.SanitizeError as Error:
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
async def ping(ctx):
  await ctx.reply('pong!')

Bot.run(Config.Bot["Discord Token"])