import discord
from discord.ext import commands
import Functions
import Classes
from unidecode import unidecode

#put it inside a try..except to catch any possible errors
try:
  Config = Classes.GetConfig()
except:
  print("\n\n\nIt looks like there has been an error in your configuration file.\n\n\n")
  raise

ItemDb = Classes.ItemList(Config.Torn["Torn API Key"])
Intents = discord.Intents.default()
Intents.message_content = True
Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)

@Bot.command()
async def search(ctx,*,SearchString:str=None):
  SearchString = unidecode(SearchString)
  try:
    Functions.SanitizeSearchTerm(SearchString)
  except Classes.SanitizeError as Error:
    if 'IllegalCharacters' in str(Error):
      await ctx.reply(embed=discord.Embed(title="Your search contains illegal characters",description="Your input contains characters that are not allowed because they aren't part of any item's name"))
      return
  if SearchString is None:
    await ctx.reply(embed=discord.Embed(title="It seems like you haven't given me any search parameters, wanna try that again?"))
  elif SearchString.isdigit():
    try:
      Embed = Functions.SearchResultEmbedConstructor([ItemDb.SearchById(SearchString)])
      await ctx.reply(embed=discord.Embed(title="**Here is your search results**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    except KeyError:
      await ctx.reply(embed=discord.Embed(title="It seems like this item ID does not exist."))
  else:
    if len(SearchString) >= 3:
      SearchResult = ItemDb.SearchByString(SearchString)
      if len(SearchResult) == 0:
        await ctx.reply(embed=discord.Embed(title="Seems like your search didn't bring up anything",description="Are you sure what you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence."))
      else:
        Embed = Functions.SearchResultEmbedConstructor(SearchResult[:5])
        await ctx.reply(embed=discord.Embed(title="**Here is your search results**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    else:
      await ctx.send(embed=discord.Embed(title="Your search term is too short",description="I am not going to look through all that could turn up in that search."))

@Bot.command()
async def ping(ctx):
  await ctx.reply('pong!')

Bot.run(Config.Bot["Discord Token"])