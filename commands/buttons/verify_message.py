from .verify_view import VerifyView
import nextcord
from nextcord.ext import commands

class Button(commands.Cog, name="Verify"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verify_persistent_view = False
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        if not self.verify_persistent_view:
            self.bot.add_view(VerifyView())
            self.verify_persistent_view = True
            print('loading persistent view')

    @commands.command()
    @commands.is_owner()
    async def verify(self, ctx: commands.Context):
        await ctx.send("Click the button below to gain access to the server.", view=VerifyView())
    
def setup(bot: commands.Bot):
    bot.add_cog(Button(bot))