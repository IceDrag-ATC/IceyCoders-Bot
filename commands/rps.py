import nextcord, random
from nextcord.ext import commands

class rps(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def rps(self, ctx, selection = None):

    if selection == None:
      await ctx.send("You must pick from `rock`, `paper`, or `scissors`.\nDo `,rps` again but with `rock`, `paper`, or `scissors`")
      return

    responses = ["Rock!", "Paper!", "Scissors!"]
    response = random.randint(0, len(responses) - 1)
      

    rps = nextcord.Embed(
      title="Rock, Paper, Scissors!",
      description="Here's the results from our game!",
      timestamp=ctx.message.created_at
    )

    rps.add_field(name="Human:", value=selection, inline=True)
    rps.add_field(name="Bot:", value=responses[response], inline=True)

    if selection.lower() == "rock" and response == 0:
      rps.add_field(name="Result:", value="It's a draw!", inline=False)

    elif selection.lower() == "paper" and response == 1:
      rps.add_field(name="Result:", value="It's a draw!", inline=False)

    elif selection.lower() == "scissors" and response == 2:
      rps.add_field(name="Result:", value="It's a draw!", inline=False)

    elif selection.lower() == "rock" and response == 1:
      rps.add_field(name="Result:", value="You lost!", inline=False)

    elif selection.lower() == "rock" and response == 2:
      rps.add_field(name="Result:", value="You won!", inline=False)

    elif selection.lower() == "paper" and response == 0:
      rps.add_field(name="Result:", value="You won!", inline=False)

    elif selection.lower() == "paper" and response == 2:
      rps.add_field(name="Result:", value="You lost!", inline=False)

    elif selection.lower() == "scissors" and response == 0:
      rps.add_field(name="Result:", value="You lost!", inline=False)

    elif selection.lower() == "scissors" and response == 1:
      rps.add_field(name="Result:", value="You won!", inline=False)

    else:
      await ctx.send("You must pick from `rock`, `paper`, or `scissors`.\nDo `,rps` again but with `rock`, `paper`, or `scissors`.")
      return


    await ctx.send(responses[response])
    await ctx.send(embed=rps)
      

def setup(client):
  client.add_cog(rps(client))