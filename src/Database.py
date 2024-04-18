from os.path import join

from sqlalchemy import create_engine,Column,Integer,Numeric,String
from sqlalchemy.orm import sessionmaker,declarative_base
from TornAPIWrapper import TornApiWrapper

from Config import Config

class DB():
  def __init__(self, DBFile: str = None):
    self.engine = create_engine(DBFile)
    self.SessionFunc = sessionmaker(bind=self.engine)
    self.session = self.SessionFunc()
    self.Base = declarative_base()
  def AddAndCommit(self, Object):
    self.session.add(Object)
    self.session.commit()
  def Commit(self):
    self.session.commit()
  def SearchByDisId(self, DiscordId: int = 0):
    return self.session.query(User).filter(User.DiscordUserId == DiscordId).first()
  def UpdateAllUsers(self):
    Query = self.session.query(User).all()
    for UserObj in Query:
      UserObj.Populate()
  def DeleteObject(self,QueryObject):
    self.session.delete(QueryObject)
    self.session.commit()

Db = DB(join("sqlite:///",Config.Bot["Database Location"]))

class User(Db.Base):
  __tablename__ = "Users"
  DiscordUserId = Column(Integer,primary_key=True)
  TornApiKey = Column(String(16),default="")
  TornUserId = Column(Integer,default=0)
  TornName = Column(String(),default="")
  TornFactionId = Column(Integer,default=0)
  TornFactionPos = Column(String(),default="")
  def Populate(self):
    if self.TornApiKey == "":
      self.TornUserId = 0
      self.TornName = ""
      self.TornFactionId = 0
      self.TornFactionPos = ""
    else:
      self.TornApi = TornApiWrapper(api_key=self.TornApiKey)
      self.TornProfileData = self.TornApi.get_user(selections=["profile"])
      self.TornUserId = self.TornProfileData["player_id"]
      self.TornName = self.TornProfileData["name"]
      self.TornFactionId = self.TornProfileData["faction"]["faction_id"]
      self.TornFactionPos = self.TornProfileData["faction"]["position"]

Db.Base.metadata.create_all(Db.engine)