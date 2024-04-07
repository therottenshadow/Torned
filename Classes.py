from TornAPIWrapper import TornApiWrapper
from datetime import datetime
from unidecode import unidecode
from Config import Config

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

class SanitizeError(Exception):
  def __init__(self,value):
    self.value = value
  def __str__(self):
    return repr(self.value)
