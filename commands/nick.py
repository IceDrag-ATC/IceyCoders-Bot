import nextcord
from nextcord.ext import commands

class Nick(commands.Cog):
    def __init__(self,client):
        self.client=client


    @commands.command(aliases=['nick', 'name'])
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self,ctx,target : nextcord.Member = None, *, nick=None):
        
        if target == None:
            target = ctx.author

        if nick == None:
            nick = target.edit(nick='')

        try:
            await target.edit(nick=f"{nick}")
            await ctx.send(f"{target.name}, was successfully changed to - `{nick}`")
        except:
            await ctx.send("Unable to edit users name.")

def setup(client):
    client.add_cog(Nick(client))