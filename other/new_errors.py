import nextcord
from nextcord.ext import commands
import datetime
dev_ids=["703578212072161280"]
class Error(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = nextcord.Embed(
              description = "This command doesn't exist.",
              color = nextcord.Color.random()
            )
            embed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=embed)
            return
        elif isinstance(error, commands.CommandOnCooldown):
            embed = nextcord.Embed(
              description = f'You are currently on cooldown! Please wait {error.retry_after:.2f}s.',
              color = nextcord.Color.random()
            )
            embed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
              description = f"You don't have the required permissions for this command. You need the `{error.missing_permissions}` permission",
              color = nextcord.Color.random()
            )
            embed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRole):
            embed = nextcord.Embed(
              description=f"You do not have the required role for this command. You need the `{error.missing_role}` role.",
              color=nextcord.Color.random()
            )
            embed.timestamp = datetime.datetime.now()
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
              description = 'DM <@703578212072161280> to report the issues!',
              color = nextcord.Color.random()
            )
            embed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=embed)
            raise error

def setup(client):
  client.add_cog(Error(client))