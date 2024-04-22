import inspect

from discord import Embed
from discord.ext import commands

from Constants import Images
import Color
from Functions import SanitizeTornKey
from Classes import SanitizeError
from Database import Db,User
from Config import Config
from cogs.background_cog import BackgroundCog

class UsersCog(commands.Cog, name='Users'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    aliases=["Verify"],
    description="This command will associate a Torn API key with your Discord user ID number, effectively bounding the API key to your Discord account on our server, which will allow you to use most of our services involving data from Torn's servers and get Discord roles applied to you depending on your faction and position within the faction.")
  async def verify(self, ctx, ApiKey: str = None) -> None:
    """Asociate a Torn API key with your Discord Account"""
    AuthorId = ctx.message.author.id
    if ApiKey is None:
      DisUser = await self.bot.fetch_user(AuthorId)
      channel = await self.bot.create_dm(DisUser)
      await channel.send(
        file=Images.ShieldCheck(),
        embed=Embed(
          title="**Verification Procedure**",
          description=inspect.cleandoc(
            """Hi,to complete the verification procedure please invoke the verify command in this DM and add a **public access** Torn API key, this key is viewable to the server owner, it is not needed to use any higher access key.

            To create an API key, you need to go to your settings page in Torn, and under API Keys you will be able to create one, otherwise, you can use [this handy link](https://www.torn.com/preferences.php#tab=api?&step=addNewKey&title=TornedDiscordBot&type=1)

            Here is an example on how to invoke the command

            `/verify a1b2c3d4e5f6g7h8`
            """),
          color=Color.Violet)
        .set_thumbnail(url=Images.AShieldCheck))
      return
    try:
      SanitizeTornKey(ApiKey)
    except SanitizeError:
      await ctx.reply(
        files=[Images.ShieldCross(),Images.TornedIcon()],
        embed=Embed(
          description="Please check that the API key you entered is a valid key, it should only contain numbers and letters and be 16 characters in length",
          color=Color.Red)
        .set_thumbnail(url=Images.AShieldCross)
        .set_author(name="Verification Failed",icon_url=Images.ATornedIcon))
      return
    Query = Db.SearchByDisId(AuthorId)
    if Query is not None and Query.TornApiKey != "":
      await ctx.reply(
        files=[Images.ShieldCross(),Images.TornedIcon()],
        embed=Embed(
          description="You are already registered on our database, you have no need to re-register",
          color=Color.Red)
        .set_thumbnail(url=Images.AShieldCross)
        .set_author(name="Verification Failed",icon_url=Images.ATornedIcon))
      return
    elif Query.DiscordUserId is not None:
      Query.TornApiKey = ApiKey
      Query.Populate()
      Db.Commit()
    else:
      InvokingUser = User(DiscordUserId=AuthorId,TornApiKey=ApiKey)
      InvokingUser.Populate()
      Db.AddAndCommit(InvokingUser)
      del InvokingUser
    DisMember = ctx.guild.get_member(AuthorId)
    await BackgroundCog.VerifyRoles(DisMember,ctx.guild)
    await ctx.reply(
      files=[Images.GreenShieldCheck(),Images.TornedIcon()],
      embed=Embed(
        description="You have been successfully verified on our database, now you should have been assigned appropiate roles and be able to use all of my services",
        color=Color.Green)
      .set_thumbnail(url=Images.AGreenShieldCheck)
      .set_author(name="Verification Successful",icon_url=Images.ATornedIcon))

  @commands.command(
    aliases=["Deverify","deauth","de-auth"],
    description="This command will remove your Torn API key from our database, allowing you to set another key or have peace of mind if you are leaving this discord")
  async def deverify(self, ctx):
    """Removes your Torn API key"""
    AuthorId = ctx.message.author.id
    Query = Db.SearchByDisId(AuthorId)
    if Query is None or Query.TornApiKey == "":
      await ctx.reply(
        files=[Images.ShieldCross(),Images.TornedIcon()],
        embed=Embed(
          description="I am sorry but it seems you haven't ever completed the verification process or you have already removed your API key.",
          color=Color.Red)
        .set_thumbnail(url=Images.AShieldCross)
        .set_author(name="De-Verification Failed",icon_url=Images.ATornedIcon))
      return
    Query.TornApiKey = ""
    Query.Populate()
    Db.Commit()
    DisMember = ctx.guild.get_member(AuthorId)
    await BackgroundCog.VerifyRoles(DisMember,ctx.guild)
    await ctx.reply(
      files=[Images.ShieldCheck(),Images.TornedIcon()],
      embed=Embed(
        description="Your Torn API key has been deleted successfully.",
        color=Color.Green)
      .set_thumbnail(url=Images.AShieldCheck)
      .set_author(name="De-Verification Completed",icon_url=Images.ATornedIcon))

async def setup(bot):
  await bot.add_cog(UsersCog(bot))