import os
import random
import discord
import pickle
import numpy as np
import requests

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author == client.user:
      return
  if message.content.startswith('$emoji'):
    print(message.attachments[0].url)
    emoji_name = message.content.split(" ")[1]
    # with open("../../../Downloads/predator.jpg", 'rb') as fd:
    img_data = requests.get(message.attachments[0].url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    with open("image_name.jpg", "rb") as img:
      img_byte = img.read()
      await message.guild.create_custom_emoji(name = emoji_name, image = img_byte)
    # with open("pic1.png", 'rb') as fd:
    #   await message.guild.create_custom_emoji(name='my_emoji', image=fd.read())



client.run(TOKEN)