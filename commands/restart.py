import nextcord
from nextcord.ext import commands
import os
dev_id=["703578212072161280"]
class Restart(commands.Cog):
  def __init__(self,client):
    self.client=client
		#can you invite me to the app

  @commands.command()
  async def restart(self,ctx):
    if str(ctx.author.id) in dev_id:
      await ctx.send("Restarting...", delete_after=2)
      await ctx.message.delete()
      for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
          if filename[:-3] != "restart":
            try:
              self.client.unload_extension(f'commands.{filename[:-3]}')
              self.client.load_extension(f'commands.{filename[:-3]}')
            except:
              self.client.load_extension(f'commands.{filename[:-3]}')
      await ctx.send("Done.", delete_after=4)
    else:
      await ctx.send("You do not have the permisison to use this command!\nThis command can only be used by the developers.")

def setup(client):
  client.add_cog(Restart(client))