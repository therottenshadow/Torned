from datetime import datetime
from typing import NoReturn
from random import randint

from TornAPIWrapper import TornApiWrapper
from unidecode import unidecode

from Config import Config


class ItemList:
  def __init__(self, TornApiKey: str):
    self.TornApi = TornApiWrapper(api_key=TornApiKey)
    self.Dic = {}
    self.UpdateTime = None
    self.NextUpdateTime = None
    self.UpdateItemList()
  def UpdateItemList(self) -> NoReturn:
    self.ApiData = self.TornApi.get_torn(selections=["items"])["items"]
    for Id in self.ApiData:
      self.Dic[Id] = self.ApiData[Id]
    self.UpdateTime = datetime.utcnow().timestamp()
    self.NextUpdateTime = datetime.utcnow().replace(
      day=datetime.utcnow().day+1,
      hour=0,
      minute=randint(1,15),
      second=0,
      microsecond=0).timestamp()
  def SearchByString(self, String: str) -> list:
    ResultList = []
    for Item in self.Dic:
      if unidecode(String).lower() in unidecode(self.Dic[Item]["name"]).lower():
        ResultList.append({Item:self.Dic[Item]})
    return ResultList
  def SearchById(self,Id: str) -> dict:
    return {Id:self.Dic[Id]}


class SanitizeError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


ItemDb = ItemList(Config.Torn["Torn API Key"])