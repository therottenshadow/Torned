import discord
from discord.ext import commands
from TornAPIWrapper import TornApiWrapper
import json
from datetime import datetime
from os.path import exists,join
from os import getcwd,stat

Cwd = getcwd()

class GetConfig:
  def __init__(self):
    self.File = self.DecideConfigFile()
    self.RawData = {}
    self.Torn = {}
    self.Bot = {}
    self.ReadFromDisk()
  def DecideConfigFile(self):
    if exists(join(Cwd,"./config_dev.json")):
      return "./config_dev.json"
    elif exists("./config.json"):
      return "./config.json"
    else:
      print("It looks like you have no config file, this code doesn't work without the needed info inside the config file. Please create 'config.json' and try again")
      exit()
  def CommitToDisk(self):
    self.Torn = self.RawData["Torn"]
    self.Bot = self.RawData["Bot"]
    with open(self.File,"w") as File:
      json.dump(self.RawData,File)
      File.close()
  def ReadFromDisk(self):
    with open(self.File,"r") as File:
      self.RawData = json.load(File)
      File.close()
    self.Torn = self.RawData["Torn"]
    self.Bot = self.RawData["Bot"]

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
  "circulation":"Circulation"
}

#put it inside a try..except to catch any possible errors
try:
  Config = GetConfig()
except:
  print("\n\n\nIt looks like there has been an error in your configuration file.\n\n\n")
  raise

class ItemList:
  def __init__(self):
    self.TornApi = TornApiWrapper(api_key=Config.Torn["Torn API Key"])
    self.Dic = {}
    self.UpdateTime = None
    self.UpdateItemList()
  def UpdateItemList(self):
    self.ApiData = self.TornApi.get_torn(selections=["items"])["items"]
    for Id in self.ApiData:
      self.Dic[Id] = self.ApiData[Id]
    self.UpdateTime = datetime.now()
  def SearchByString(self,String: str):
    ResultList = []
    for Item in self.Dic:
      if String.lower() in self.Dic[Item]["name"].lower():
        ResultList.append({Item:self.Dic[Item]})
    return ResultList
  def SearchById(self,Id: str):
    return {Id:self.Dic[Id]}

def SearchResultEmbedConstructor(ResultList):
  ResultingEmbed = {"Message":"","ImageUrl":""}
  for Result in ResultList:
    for ResultId in Result:
      for x in Result[ResultId]:
        if x == "image" and ResultingEmbed["ImageUrl"] == "":
          ResultingEmbed["ImageUrl"] = Result[ResultId][x]
        elif x == "image" and not(ResultingEmbed["ImageUrl"] == ""):
          pass
        elif x == "name":
          ResultingEmbed["Message"] += f'**{Result[ResultId][x]}**\n'
        elif not((Result[ResultId][x] is None) or (Result[ResultId][x] == "")):
          ResultingEmbed["Message"] += f'**{ApiTranslate[x]}**: {Result[ResultId][x]}\n'
      ResultingEmbed["Message"] += "\n"
  return ResultingEmbed

ItemDb = ItemList()
Intents = discord.Intents.default()
Intents.message_content = True
Bot = commands.Bot(command_prefix=Config.Bot["Command Prefix"],intents=Intents)

@Bot.command()
async def search(ctx,*,SearchString:str=None):
  if SearchString is None:
    await ctx.reply(embed=discord.Embed(title="It seems like you haven't given me any search parameters, wanna try that again?"))
  elif SearchString.isdigit():
    try:
      Embed = SearchResultEmbedConstructor([ItemDb.SearchById(SearchString)])
      await ctx.reply(embed=discord.Embed(title="**Here is your search results**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    except KeyError:
      await ctx.reply(embed=discord.Embed(title="It seems like this item ID does not exist."))
  else:
    if len(SearchString) >= 3:
      SearchResult = ItemDb.SearchByString(SearchString)
      if len(SearchResult) == 0:
        await ctx.reply(embed=discord.Embed(title="Seems like your search didn't bring up anything",description="Are you sure what you searched exists?? If it is something new it can take up to 6 hours for me to acknowledge it's existence."))
      else:
        Embed = SearchResultEmbedConstructor(SearchResult[:5])
        await ctx.reply(embed=discord.Embed(title="**Here is your search results**",description=Embed["Message"]).set_thumbnail(url=Embed["ImageUrl"]))
    else:
      await ctx.send("Your search term is too short, I am not going to look through all that could turn up in that search.")

@Bot.command()
async def ping(ctx):
  await ctx.reply('pong!')

Bot.run(Config.Bot["Discord Token"])