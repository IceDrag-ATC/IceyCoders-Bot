from .sr_view import SRView
import nextcord
from nextcord.ext import commands

class Button(commands.Cog, name="SR"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sr_persistent_view = False
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.sr_persistent_view:
            self.bot.add_view(SRView())
            self.sr_persistent_view = True
            print('loading persistent view')

    @commands.command()
    @commands.is_owner()
    async def sr(self, ctx: commands.Context):
        embed = nextcord.Embed(
            title = "Self Roles",
            description="Get your very own self roles here, Look at the list below for some options on what to pick.",
            color=nextcord.Color.fuchsia()
        )
        await ctx.send(embed=embed, view=SRView())
    
def setup(bot: commands.Bot):
    bot.add_cog(Button(bot))