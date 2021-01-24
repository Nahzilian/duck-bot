import discord
import asyncio
from main import chat
from config import api_key
from logger import db_logger, discord_chat
client = discord.Client()

learn = False

@client.event
async def on_message(message):
    # if learn:
    
    if message.author == client.user:
        return
    response = chat(message.content)
    if response == 'Wdym?':
        learn = True
    discord_chat(response,message)
    await message.channel.send(response)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    db_logger("Logged in as {name}".format(name = client.user.name))


client.run(api_key)