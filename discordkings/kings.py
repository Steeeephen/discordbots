# bot.py
import os
import random
import discord
import pickle
import numpy as np

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

rules = {
  1:'Waterfall',2:'You',3:'Me',4:'Whores',5:'Dive',6:'Dicks',7:'Heaven',
  8:'Mate',9:'Rhyme',10:'Never Have I Ever',11:'Rule',12:'Questionmaster',13:'King'
}

names = dict()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  if message.content.startswith('$kings'):
    players = (message.content.split(' ')[1:])

    for player in players:
      names[player] = 0

    if(players):
      with open('players', 'wb') as fp:
          pickle.dump(players, fp)

      x1=['H','S','C','D']
      x = np.repeat(x1, 13).tolist()
      y = list(range(1,14))*4

      cards = ["%d%s" % (x1,y1) for (x1,y1) in list(zip(y,x))]

      random.shuffle(cards)
      with open('cards', 'wb') as fp:
          pickle.dump(cards, fp)

      with open('kings', 'wb') as fp:
          pickle.dump(0, fp)
      await message.channel.send("Players playing: %s\n Turn: %s \nType $card to draw a card" % (', '.join([player for player in players]),players[0]))
    else:
      await message.channel.send("No players selected")

  if message.content.startswith('$card'):  
    with open ('players', 'rb') as fp:
        players = pickle.load(fp)
    try:
      player = players[0]
    except:
      await message.channel.send("No players selected")

    if message.author.id == names[player]:  
      players = players[1:]
      players.append(player)

      with open('cards', 'rb') as fp:
          cards = pickle.load(fp)
      try:
        card = cards.pop()
      except:
        await message.channel.send("No more cards left")

      with open('kings','rb') as fp:
              kings = int(pickle.load(fp))
          
      if(int(card[:-1]) == 13):
          kings += 1
          if(kings == 4):
              await message.channel.send("Winner: %s" % players[0])    
          else:
              with open('kings', 'wb') as fp:
                  pickle.dump(kings, fp)
      
      with open('cards', 'wb') as fp:
          pickle.dump(cards, fp)
      with open('players', 'wb') as fp:
          pickle.dump(players, fp)

      await message.channel.send(file=discord.File('card_images/%s.png' % card))
      await message.channel.send("Player: %s" % players[0])
    else:
      await message.channel.send("Wait your turn")

  if message.content.startswith('$name'):
    await message.channel.send("%s is %s" % (message.author, message.content.split(' ')[1]))
    names[message.content.split(' ')[1]] = message.author.id
    print(names)
    

client.run(TOKEN)