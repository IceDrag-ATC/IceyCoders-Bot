import nextcord
from nextcord.ext import commands, tasks
import psutil

us = 0
um = 0
uh = 0
ud = 0

class stats(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.uptimeCounter.start()

  @tasks.loop(seconds=2.0)
  async def uptimeCounter(self):
    global us, um, uh, ud
    us += 1
    if us == 60:
      us = 0
      um += 1
      if um == 60:
        um = 0
        uh += 1
        if uh == 24:
          uh = 0
          ud += 1
  
  @uptimeCounter.before_loop
  async def beforeUptimeCounter(self):
    print("Waiting....")
    await self.client.wait_until_ready()
    print("Done")

  @commands.command()
  async def uptime(self,ctx):
    global us, um, uh, ud
    embed = nextcord.Embed(
      title="Uptime Status",
      description=f"I have been on line for `{ud}` days, `{uh}` hours, `{um}` minutes and `{us}` seconds!",
      color=nextcord.Color.random()
    )
    await ctx.send(embed=embed)

  @commands.command()
  async def usage(self, ctx):
    embed=nextcord.Embed(
      title=f"IceyCoders Bot Usage",
      description="Here is a view of all of the CPU and RAM that the IceyCoders bot is using.",
      color=nextcord.Color.random()
    )
    embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=True)
    embed.add_field(name="RAM", value=f"{psutil.virtual_memory()[2]}")
    await ctx.send(embed=embed)


def setup(client):
  client.add_cog(stats(client))