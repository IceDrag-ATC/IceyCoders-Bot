import nextcord
from nextcord.ext import commands
dev_ids=["703578212072161280"]
class Error(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = nextcord.Embed(
              title = ':x: NO COMMAND FOUND :x:',
              description = 'There is no command with that name.',
              color = nextcord.Color.red()
            )
            await ctx.reply(embed=embed)
            return
        elif isinstance(error, commands.CommandOnCooldown):
            embed = nextcord.Embed(
              title = ':x: COOLDOWN :x:',
              description = f'You are currently on cooldown! Please wait {error.retry_after:.2f}s.',
              color = nextcord.Color.red()
            )
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(
              title = ":x: NO PERMISSIONS :x:",
              description = f"You don't have the required permissions for this command. You need the `{error.missing_permissions}` permission",
              color = nextcord.Color.red()
            )
            await ctx.reply(embed=embed)
        elif isinstance(error, commands.MissingRole):
            embed = nextcord.Embed(
              title=":x: MISSING ROLE :x:",
              description=f"You do not have the required role for this command. You need the `{error.missing_role}` role.",
              color=nextcord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
              title = ':x: ISSUE FOUND :x:',
              description = 'DM <@703578212072161280> to report the issues!',
              color = nextcord.Color.red()
            )
            await ctx.reply(embed=embed)
            raise error

def setup(client):
  client.add_cog(Error(client))