import nextcord
from nextcord.ext import commands

class Purge(commands.Cog):
  def __init__(self, client):
      self.client = client

  @commands.command(aliases=['p'])
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, amount=None):
    if amount == None:
      await ctx.send('Please enter an amount of messages to purge', delete_after=5)
    elif int(amount) <= 0:
      await ctx.send('Amount cannot be negative or 0')
    else:
      await ctx.channel.purge(limit=int(amount) + 1)
      await ctx.send(f'Cleared `{amount}` messages! This was done by {str(ctx.author.mention)}.', delete_after=10)


def setup(client):
  client.add_cog(Purge(client))