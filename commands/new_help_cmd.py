import nextcord
from nextcord.ext import commands
import asyncio, datetime
from asyncio import sleep
from typing import Optional, Set

class HelpSelect(nextcord.ui.Select):
    def __init__(self):
        selectoptions = [
            nextcord.SelectOption(label="Moderation", description="Commands that staff are only allowed to use", emoji="🔨"),
            nextcord.SelectOption(label="Helpful", description="Gives a list of commands that will be usefull", emoji="✋"),
            nextcord.SelectOption(label="Random", description="Shows a list of the commands that are completly random", emoji="🙃"),
            nextcord.SelectOption(label="Owner Only", description="Commands that only the owner can use", emoji="❌")
        ]
        super().__init__(placeholder="Select an help selection", min_values=1, max_values=1, options=selectoptions)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Moderation":
            embed=nextcord.Embed(
                title=f"Moderation Information" , 
                description="Here you can find the commands of moderation (staff only). D = Dyno, I = Iceycoders Bot",
                color=nextcord.Color.green()
            )

            embed.add_field(name="Ban - D", value="Bans the user depending on the reason and duration, you can appeal this.",inline=True)
            embed.add_field(name="Kick - D", value="Kicks the user from the server but, they are able to join back with an invite.",inline=True)
            embed.add_field(name="Mute - D",value="Mutes the user making them unable to join/type in chats, you can appeal this.",inline=True)
            embed.add_field(name="Warn - D",value="Warns the user depending on what they do, this has no serious actions.",inline=True)
            embed.add_field(name="Purge - I",value="Bulks messages in a certain radius.",inline=True)
            embed.add_field(name="Addrole - I", value="Adds a rike ti a specific member.",inline=True)
            embed.add_field(name="Remrole - I",value="Removes a role from a specific member.",inline=True)
            embed.add_field(name="Slowmode - I",value="Sets a cooldown after every message you send.",inline=True)
            embed.add_field(name="Moderate - I",value="Changes the users nickname as they have special characters in it.",inline=True)
            
            embed.set_footer(text='End of Moderation help section.')

            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "Helpful":
            embed=nextcord.Embed(
                title="Helpful Information",
                description="Here you can find commands that may be helpful towards you. All of these commands are custom.",
                color=nextcord.Color.yellow()
            )
    
            embed.add_field(name="RTFM", value="Retrieves documentation on the nextcord/python libaries.",inline=True)
            embed.add_field(name="Report", value="Sends you a link where you can write a complaint about a member.",inline=True)
            embed.add_field(name="Aboutme", value="Hows information about the bot.",inline=True)
           
            embed.set_footer(text= 'End of Helpful help section')

            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "Random":
            embed=nextcord.Embed(
                title="Random Information",
                description="Here you can find commands that are just completly random towards the server, if they have 'Fun Command' next to them it means they are just random not serious.",
                color=nextcord.Color.magenta()
            ) 
    
            embed.add_field(name="Membercount", value="Shows you how many members are in the server.",inline=True)
            embed.add_field(name="Serverinfo", value="Shows you server stats (Region, Owner, Channles, etc).",inline=True)
            embed.add_field(name="Nickname", value="Changes your nickname to what you want. You need the manage nick names permission, but something new that relates to this will be coming soon.",inline=True)
            embed.add_field(name="Gayrate", value="Fun command - Shows a random percentage on how gay you are.",inline=True)
            embed.add_field(name="Pp", value="Fun command - Shows a random size on how big your pp is.,inline=True")
            embed.add_field(name="Rps", value="Rock paper scissors - Have a game with the bot.",inline=True)
            embed.add_field(name="Uptime", value="Shows how long the bot has been online for.",inline=True)
            embed.add_field(name="Usage", value="Shows you the usages of ram, cpu the bot uses.",inline=True)
            embed.add_field(name="Ping", value="Shows you the delay for the bot to respong.",inline=True)
            embed.add_field(name="Help", value="What you are seeing right this second.",inline=True)

   
            embed.set_footer(text='End of Random help section')

            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "Owner Only":
            embed=nextcord.Embed(
                title="Owner Only Information",
                description="Shows commands that only the owner can use.",
                color=nextcord.Color.orange()
            )

            embed.add_field(name="Eval", value="Sends stuff thats in a code block.",inline=True)
            embed.add_field(name="Sr",value="Self Role Buttons.",inline=True)
            embed.add_field(name="Verify",value="Verify Button.",inline=True)
   
            embed.set_footer(text='End of Owner Only help section')

            await interaction.response.edit_message(embed=embed)

        else:
            embed=nextcord.Embed(
                title="Help menu error!",
                description="This can be a bug or a wrong command, Please report this to the bot owner.",
                color=nextcord.Color.red()
            )

            owner = 703578212072161280
            dm = await owner.create_dm()
            embed = nextcord.Embed(
                title="Alert!",
                description=f"Hey, one of the options in the help command called: {self.values[0]}, has ran in to an error!",
                color = nextcord.Color.red()
            )
            await dm.send(embed=embed)
            await interaction.response.edit_message(embed=embed)

class HelpView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.add_item(HelpSelect())

class HelpCmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['help', 'HELP'])
    @nextcord.ext.commands.guild_only()
    async def Help(self, ctx):
        view1=HelpView()
        embed=nextcord.Embed(
            title="Help",
            description="These are the command in the server that you can use, use the selection box at the bottom to navigate to other categorys.\n\n🔨 - Moderation\n\n✋ - Helpful\n\n🙃 - Random\n\n❌ - Owner Only",
            color=nextcord.Color.fuchsia()
        )
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed, view=view1)


def setup(client):
    client.add_cog(HelpCmd(client))