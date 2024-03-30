from TornAPIWrapper import TornApiWrapper
from datetime import datetime
import json
from os.path import exists,join
from os import getcwd,stat
from unidecode import unidecode

class GetConfig:
  def __init__(self):
    self.Cwd = getcwd()
    self.File = self.DecideConfigFile()
    self.RawData = {}
    self.Torn = {}
    self.Bot = {}
    self.ReadFromDisk()
  def DecideConfigFile(self):
    if exists(join(self.Cwd,"./config_dev.json")):
      return "./config_dev.json"
    elif exists(join(self.Cwd,"./config.json")):
      return "./config.json"
    else:
      print("It looks like you have no config file, this code doesn't work without the needed info inside the config file. Please create 'config.json' and try again")
      exit()
  def CommitToDisk(self):
    self.RawData["Torn"] = self.Torn
    self.RawData["Bot"] = self.Bot
    with open(self.File,"w") as File:
      json.dump(self.RawData,File)
      File.close()
  def ReadFromDisk(self):
    with open(self.File,"r") as File:
      self.RawData = json.load(File)
      File.close()
    self.Torn = self.RawData["Torn"]
    self.Bot = self.RawData["Bot"]

class ItemList:
  def __init__(self,TornApiKey: str):
    self.TornApi = TornApiWrapper(api_key=TornApiKey)
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
      if unidecode(String).lower() in unidecode(self.Dic[Item]["name"]).lower():
        ResultList.append({Item:self.Dic[Item]})
    return ResultList
  def SearchById(self,Id: str):
    return {Id:self.Dic[Id]}