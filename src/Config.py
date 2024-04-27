import json
from os.path import exists,join
from os import getcwd

class GetConfig:
  def __init__(self):
    self.Cwd = getcwd()
    self.File = self.DecideConfigFile()
    self.RawData = {}
    self.Torn = {}
    self.Bot = {}
    self.UserMan = {}
    self.Modules = {}
    self.MiscModConf = {}
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
    self.RawData["User Management"] = self.UserMan
    self.RawData["Modules"] = self.Modules
    self.RawData["Misc Module Config"] = self.MiscModConf
    with open(self.File,"w") as File:
      json.dump(self.RawData,File)
      File.close()
  def ReadFromDisk(self):
    with open(self.File,"r") as File:
      self.RawData = json.load(File)
      File.close()
    self.Torn = self.RawData["Torn"]
    self.Bot = self.RawData["Bot"]
    self.UserMan = self.RawData["User Management"]
    self.Modules = self.RawData["Modules"]
    self.MiscModConf = self.RawData["Misc Module Config"]

try:
  Config = GetConfig()
except:
  print("\n\n\nIt looks like there has been an error in your configuration file or it doesn't exist.\n\n\n")
  raise