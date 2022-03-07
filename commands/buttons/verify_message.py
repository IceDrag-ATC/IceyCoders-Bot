from .verify_view import VerifyView
import nextcord
from nextcord.ext import commands

ownerRole = 942457163614400613

class Button(commands.Cog, name="Verify"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verify_persistent_view = False
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.verify_persistent_view:
            self.bot.add_view(VerifyView())
            self.verify_persistent_view = True
            print('loading persistent view')

    @commands.command()
    @commands.is_owner()
    async def verify(self, ctx: commands.Context):
        if ownerRole in[r.id for r in ctx.author.roles]:
            await ctx.send("Click the button below to gain access to the server.", view=VerifyView())
        else:
            await ctx.send("This command is for the owner only!")

def setup(bot: commands.Bot):
    bot.add_cog(Button(bot))