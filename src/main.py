from os import listdir
from datetime import datetime
from time import sleep
from threading import Thread,Event
from datetime import datetime
from typing import NoReturn

import discord
from discord.ext import commands

from Config import Config
from Classes import ItemDb
from Database import Db

CogsList = [
  "discord_cog",
  "torn_cog",
  "users_cog",
  "bot_cog"
]


class Scheduled:
  pass


class Timed:
  UserUpdateTime = 0
  UserNextUpdateTime = 0

  def run(RunEvent) -> NoReturn:
    while(RunEvent.is_set()):
      sleep(5)
      Timed.UpdateItemDb()
      Timed.UpdateUserDb()
  def UpdateItemDb() -> NoReturn:
    if (ItemDb.NextUpdateTime <= datetime.utcnow().timestamp()
        or datetime.utcnow().timestamp() - ItemDb.UpdateTime > 88200):
      ItemDb.UpdateItemList()
  def UpdateUserDb() -> NoReturn:
    if (Timed.UserNextUpdateTime <= datetime.utcnow().timestamp()
        or datetime.utcnow().timestamp() - Timed.UserUpdateTime > 4000):
      Db.UpdateAllUsers()
      Timed.UserUpdateTime = datetime.utcnow().timestamp()
      hour = datetime.utcnow().hour + 1
      if hour > 23:
        hour -= 24
        day = datetime.utcnow().day + 1
      else:
        day = datetime.utcnow().day
      Timed.UserNextUpdateTime = datetime.utcnow().replace(
        day=day,
        hour=hour,
        minute=0,
        second=0
        ).timestamp()


def main():
  Intents = discord.Intents.default()
  Intents.message_content = True
  Bot = commands.Bot(command_prefix = Config.Bot["Command Prefix"],intents = Intents)

  @Bot.event
  async def on_ready():
    for Cog in CogsList:
      await Bot.load_extension(f"cogs.{Cog}")

  run_event = Event()
  run_event.set()
  Threads = []
  Threads.append(Thread(target = Timed.run, args = (run_event,)))
  Threads.append(Thread(target = Bot.run, args = (Config.Bot["Discord Token"],)))

  for thread in Threads:
    sleep(0.5)
    thread.start()
  try:
    while(True):
      sleep(1)
  except KeyboardInterrupt:
    run_event.clear()
    for thread in Threads:
      ThreadIndex = Threads.index(thread)
      ThreadsLen = len(Threads) - (ThreadIndex + 1)
      print(f'Stopping thread {ThreadIndex}. Maximum wait is 5 seconds unless this is the last thread (threads left = 1)')
      try:
        thread.join()
      except KeyboardInterrupt:
        pass
      print(f'Thread {ThreadIndex} stopped. Threads left: {ThreadsLen}')
    quit()

if __name__ == "__main__":
  main()