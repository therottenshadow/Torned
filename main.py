import discord
from discord.ext import commands
import configparser
from datetime import datetime
from TornAPIWrapper import TornApiWrapper
import random

ConfigFile = configparser.ConfigParser()
ConfigFile.read('config_dev.ini')

#put it inside a try..except to catch any possible errors
try:
	Config = {
			"TornApi":								ConfigFile["Torn"]["dev_torn_api_key"],
			"DiscordToken":						ConfigFile["Bot"]["discord_token"],
			"CommandPrefix": 					ConfigFile["Bot"]["command_prefix"]
	}
except:
	print("\n\n\nIt looks like there has been an error in your configuration file.\n\n\n")
	raise

class ItemList:
	def __init__(self):
		self.TornApi = TornApiWrapper(api_key=Config["TornApi"])
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
		return self.Dic[Id]

ItemDb = ItemList()
Bot = commands.Bot(command_prefix=Config["CommandPrefix"])

@Bot.command()
async def search(ctx,*,SearchString:str=None):
	if SearchString is None:
		await ctx.send("It seems like you haven't given me any search parameters, wanna try that again?")
	elif SearchString.isdigit():
		try:
			await ctx.send(ItemDb.SearchById(SearchString))
		except KeyError:
			await ctx.send("It seems like this item ID does not exist.")
	else:
		if len(SearchString) >= 3:
			ResultCounter = 0
			ResultMsg = "This is what I have found:\n"
			SearchResult = ItemDb.SearchByString(SearchString)
			if len(SearchResult) == 0:
				await ctx.send("Seems like your search didn't bring up anything")
			else:
				for Item in SearchResult:
					if ResultCounter > 4:
						break
					ResultCounter += 1
					ResultMsg += Item[[Id for Id in Item][0]]['name']
					ResultMsg += "\n"
				await ctx.send(ResultMsg)
		else:
			await ctx.send("""Your search term is too short, please don't make me
                  look through all that could turn up in that search.""")

@Bot.command()
async def ping(ctx):
	await ctx.send('pong!')

Bot.run(Config["DiscordToken"])