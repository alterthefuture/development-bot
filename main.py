from pymongo import MongoClient
from discord.ext import commands
import discord
import os

# Connecting to database
cluster = MongoClient("mongo-link")
db = cluster["your-cluster"]
collection = db["your-collection"]

your_id = 23131123

# Creating bot
intents=discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),intents=intents,owner_id=your_id)
bot.remove_command(name="help")

# Bot Events
@bot.event
async def on_connect():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"Starting..."))

@bot.event
async def on_ready():
    print("> Alters Helper bot is online.")

    channel = bot.get_channel(879241506408513566)
    await channel.edit(name=f"Members: {len(bot.users)}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"Alters Development!"))

@bot.event
async def on_message(message):
	if message.channel.id == 879241056842043412 or message.channel.id == 879238478175555650:
		await message.delete()

	await bot.process_commands(message)

# Loading Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Starting Bot
bot.run("token-here")
