import nextcord
from nextcord.ext import commands


class Slowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['sm'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int=0):
        await ctx.channel.edit(slowmode_delay=seconds)
    
        sm = nextcord.Embed(
          title="SlowMode Complete",
          description=f"I have set the slowmode to `{seconds}`.",
          colour=nextcord.Colour.random()
        )

        await ctx.reply(embed=sm)


def setup(client):
  client.add_cog(Slowmode(client))
