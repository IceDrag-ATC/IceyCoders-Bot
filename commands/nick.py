import nextcord
from nextcord.ext import commands

class Nick(commands.Cog):
    def __init__(self,client):
        self.client=client


    @commands.command(aliases=['nick', 'name'])
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self,ctx,*, nick=None):
        if nick == None:
            nick = ctx.author.edit(nick=None)

        try:
            await ctx.author.edit(nick=f"{nick}")
            await ctx.send(f"{ctx.author.name}, was successfully changed to - `{nick}`")
        except:
            await ctx.send("Unable to edit users name.")

def setup(client):
    client.add_cog(Nick(client))