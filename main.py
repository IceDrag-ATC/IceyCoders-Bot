import nextcord
from nextcord.ext import commands
import os, inspect, datetime, time, json, asyncio, random, psutil, aiohttp
from dotenv import load_dotenv
from commands.buttons.verify_view import VerifyView
from commands.buttons.sr_view import SRView

load_dotenv()

us = 0
um = 0
uh = 0
ud = 0

ownerRole = 703578212072161280

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
intents = nextcord.Intents.all()
client = commands.Bot(command_prefix=',',owner_id=703578212072161280, intents=intents)
start_time = time.time()
client.remove_command('help')
client.persistent_views_added = False

@client.event
async def on_ready():
    print(f"Logged in as {client.user}. IceyCoders Bot currently has {client.guilds[0].member_count} members.")
    await client.change_presence(activity=nextcord.Activity(
        type=nextcord.ActivityType.watching,
        name=f"{client.guilds[0].member_count} Members | ,help"))
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            client.load_extension(f'commands.{filename[:-3]}')
    #if a command is in a folder that is with in a folder do client.load_extension(f'commands.(foldername).(filename)')
    client.load_extension("commands.buttons.verify_message")
    client.load_extension("commands.buttons.sr_message")
    if not client.persistent_views_added:
        client.add_view(VerifyView())
        client.add_view(SRView())
    client.persistent_views_added = True
    print('loading persistent views')


@client.listen()
async def on_member_join(member: nextcord.Member):
    guild = member.guild
    role = guild.get_role(942461297465909318)
    channel = client.get_channel(942809091401744524)
    await member.add_roles(role)
    await channel.send(f"{member.mention} Has joined the server! Please read <#942470239633961002> before verifying in <#942470122902265856>.")
    print (f"{member.name}, {member.id}. Member count - {client.guilds[0].member_count}")


#Ping


@client.command(aliases=['ms'])
async def ping(ctx):
    embed = nextcord.Embed(title='Pong!',
      description=f'🏓 {round(client.latency * 1000)}ms',
      color=nextcord.Color.blue())
    await ctx.send(embed=embed)

@client.command(name='eval',pass_context=True)
async def eval_(ctx, *, command):
  if ownerRole in[r.id for r in ctx.author.roles]:
    try:
      res = eval(command)
      embed = nextcord.Embed(
        title = 'Evaluated',
        color = nextcord.Color.green()
      )
      embed.add_field(name = '📥 Input', value = f'```\n{command}\n```')
      embed.add_field(name = '📤 Output', value = f'```\n{res}\n```')
      await ctx.send(embed = embed)
      if inspect.isawaitable(res):
        await ctx.send(await res, delete_after=0.001)
      else:
        await client.send(res, delete_after=0.001)

    except Exception:
      pass
  else:
    await ctx.send("This command if for the owner only!")

async def startup():
    client.session = aiohttp.ClientSession()



client.loop.create_task(startup())
client.run(os.environ['DISCORD_TOKEN'])
