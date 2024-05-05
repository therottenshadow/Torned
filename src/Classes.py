"""File where classes are defined"""

from typing import NoReturn
from random import randint

from TornAPIWrapper import TornApiWrapper
from unidecode import unidecode

from Config import Config


class ItemList:
  def __init__(self, TornApiKey: str):
    self.TornApi = TornApiWrapper(api_key=TornApiKey)
    self.Dic = {}
    self.UpdateItemList()
  def UpdateItemList(self) -> NoReturn:
    self.ApiData = self.TornApi.get_torn(selections=["items"])["items"]
    for Id in self.ApiData:
      self.Dic[Id] = self.ApiData[Id]
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
