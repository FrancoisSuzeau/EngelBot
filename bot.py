# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pandas as pd 
from packages.intelligencia import Intelligencia as IN
from packages.member import Member as MB
from packages.superadmin import SuperAdmin as SP
from packages.tasks import Tasks as T

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PICTURES_PATH = os.getenv('PICTURES_PATH')
DATA_PATH = os.getenv('DATA_PATH')

intents = discord.Intents.default()
intents.message_content = True
help_command = commands.DefaultHelpCommand(no_category='Default')
bot = commands.Bot(command_prefix='!', intents=intents, help_command=help_command)
df = pd.read_csv(DATA_PATH + "backup.csv", header=None, delimiter=';')
df[0] = df[0].astype('string')
sentences = df[0].to_dict()
MyIn = IN()

# ------------------------------------------------------------------------------- SERVER EVENT -----------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    channels = []
    print(f'{bot.user} is connected to the following guild:')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        for channel in guild.channels:
            if "engelbot" in channel.name:
                print(f'(Channel: {channel.name})')
                channels.append(channel)

    MyT = T(bot=bot, channels=channels)

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Living my life"))
    await bot.add_cog(SP(bot=bot, sentences=sentences, MyIn=MyIn, MyT=MyT))
    await bot.add_cog(MB(bot=bot, sentences=sentences, PICTURES_PATH=PICTURES_PATH, DATA_PATH=DATA_PATH))
    await bot.add_cog(MyT)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Vous ne pouvez pas faire ça, vous n\'avez pas le droit. Il faut que vous consultiez le registre.')

# ===========================================================================================================================================================================================
bot.run(DISCORD_TOKEN)
# ===========================================================================================================================================================================================