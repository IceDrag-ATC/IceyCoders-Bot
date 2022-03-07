import nextcord
from nextcord.ext import commands
import random, string, datetime


class moderate(commands.Cog):
  def __init__(self,client):
    self.client=client

  @commands.command(
    name="censor",
    description="Used to censor a users name",
    aliases=['moderate','mod']
    )
  @commands.guild_only()
  @commands.has_permissions(manage_nicknames=True)
  async def censor(self, ctx, target : nextcord.Member = None):
    
    if target is None:
      await ctx.send("Please supply a user to censor the username of.")
      return

    nick = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

    try:
      guild = ctx.guild
      dm = await target.create_dm()
      embed = nextcord.Embed(
        title = "Alert",
        description=f"Your have been moderated in {guild.name}, as your name has some special characters in it. If you want your name back go to <#922961486937206804> and do `!verify` to get your name back."
      )
      await dm.send(embed=embed)
    except:
      pass

    try:
      embed = nextcord.Embed(
        title = "Moderate Success",
        description = f"The user of {target.name} was successfully moderated!",
        color = nextcord.Color.green()
      )
      embed.add_field(name="Before", value=f"```{target.name}```", inline=False)
      embed.add_field(name="After", value=f"```Moderated Nickname {nick}```", inline=False)
      embed.timestamp = datetime.datetime.now()
      await target.edit(nick=f"Moderated Nickname {nick}")
      await ctx.send(embed=embed)
    except:
      await ctx.send("I can't edit that user's nickname.")
    
  @commands.command(aliases=['unmod', 'unmoderate', 'uncensor'])
  @commands.guild_only()
  @commands.has_permissions(manage_nicknames=True)
  async def reset(self, ctx, target : nextcord.Member = None):

    if target is None:
      await ctx.send("Please supply a user/id to reset their username.")
      return
    
    nick = ''

    try:
      await target.edit(nick=f"{nick}")
      await ctx.send(f"{target.name}, was successfully reset.")
    except:
      await ctx.send("I can't edit that user's nickname.")

def setup(client):
  client.add_cog(moderate(client))