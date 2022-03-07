from .sr_view import SRView
import nextcord
from nextcord.ext import commands

ownerRole = 942457163614400613

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
    async def sr(self, ctx: commands.Context):
        if ownerRole in[r.id for r in ctx.author.roles]:
            embed = nextcord.Embed(
                title = "Self Roles",
                description="Get your very own self roles here, Look at the list below for some options on what to pick.",
                color=nextcord.Color.fuchsia()
            )
            await ctx.send(embed=embed, view=SRView())
        else:
            await ctx.send("This command is for the owner only!")
    
def setup(bot: commands.Bot):
    bot.add_cog(Button(bot))