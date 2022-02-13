import nextcord
from nextcord.ext import commands

class Roles(commands.Cog):
  def __init__(self,client):
    self.client=client
  
  @commands.command(aliases=['arole'])
  @commands.has_permissions(manage_roles=True)
  async def addrole(self,ctx,member:nextcord.Member,*, role:nextcord.Role):
    await member.add_roles(role)
    embed=nextcord.Embed(
        title="Role Added ✅",
        description=f"Successfully Added the {role.mention} to {member}",
        color=nextcord.Color.green()
    )
    await ctx.send(embed=embed)
    
  @commands.command(aliases=['rrole', 'removerole'])
  @commands.has_permissions(manage_roles=True)
  async def remrole(self,ctx,member:nextcord.Member,*,role:nextcord.Role):
    await member.remove_roles(role)
    embed=nextcord.Embed(
        title="Role Removed ❌",
        description=f"Successfully Removed the {role.mention} from {member}",
        color=nextcord.Color.red()
    )
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Roles(client))