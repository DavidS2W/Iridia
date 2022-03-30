import discord
import requests
import json
import random
import wikipedia
import asyncio
from datetime import datetime
import pytz
from discord.ext import commands
from disputils import BotEmbedPaginator
import upsidedown
import googlesearch
from bs4 import BeautifulSoup
import wolframalpha
from googletrans import Translator
from youtube_search import YoutubeSearch
from discord.utils import get
from discord import FFmpegPCMAudio
from lyrics_extractor import SongLyrics
from youtube_dl import YoutubeDL
import pymongo


mongoclient = pymongo.MongoClient("mongodb+srv://davidswsim:ds2wds2w@ds2w-clusters.7sbca.mongodb.net/DS2W-Clusters?retryWrites=true&w=majority")
mydb = mongoclient["Iridia_1"]
file = mydb["server_info"]

def get_prefix(client, message):
  try:
    get_prefix = file.find_one({"_id": message.guild.id})["prefix"]
    return get_prefix
  except:
    print(message.guild.name)


client = commands.Bot(command_prefix= get_prefix, intents=discord.Intents.all())

client.remove_command('help')

client.get_guild(id)

prefix = 'i'

animal_words = ["dog", "cat", "fox", "koala", "panda"]


dice_pics = ['<:d6:806019379774226452>', '<:d5:810328229444452363>', '<:d4:806019355996979231>', '<:d3:810328197484118017>', '<:d2:806019324804333568>', '<:d1:810328161127497778>']

orwellian_quotes = ["Doublethink means the power of holding two contradictory beliefs in one's mind simultaneously, and accepting both of them.", "If you loved someone, you loved him, and when you had nothing else to give, you still gave him love.", "Power is in tearing human minds to pieces and putting them together again in new shapes of your own choosing.", "One does not establish a dictatorship in order to safeguard a revolution; one makes the revolution in order to establish the dictatorship.", "The masses never revolt of their own accord, and they never revolt merely because they are oppressed. Indeed, so long as they are not permitted to have standards of comparison, they never even become aware that they are oppressed.", "Being in a minority, even in a minority of one, did not make you mad. There was truth and there was untruth, and if you clung to the truth even against the whole world, you were not mad.", "Freedom is the freedom to say that two plus two make four. If that is granted, all else follows.", "For, after all, how do we know that two and two make four? Or that the force of gravity works? Or that the past is unchangeable? If both the past and the external world exist only in the mind, and if the mind itself is controllable – what then?", "Confession is not betrayal. What you say or do doesn't matter; only feelings matter. If they could make me stop loving you-that would be the real betrayal.", "Big brother is watching you.", "War is peace", "Freedom is slavery"]

coin_words = ["heads", "tails"]

eightball_words = ["Definitely not", "I don't think so", "no", "maybe", "absolutely", "of course", "yes", "unsure, ask again"]

tragic_events = ["accidentally cycled into the drain.", "was taken to see a horror film and couldn't stand it, crying and screaming the whole time.", "caught COVID-19 and died.", "ran off a cliff trying to fly.", "was conscripted to join the army during World War 3.", "was hit by a falling brick from a construction site.", "was bitten by a king cobra.", "stuck a fork into a socket and died from electrocution.", "kissed a girl and caught COVID-19.", "ate uncooked meat and died.", "had a nervous breakdown in public.", "died.", "was hit by a stray bullet.", "is now being chased by a tiger.", "shat in public."]

plane_words = ["crashing into a sofa.", "landing in the toilet bowl.", "getting snatched out of the air by someone.", "ramming into a fragile vase and knocking it over.", "landing in a cup of water.", "hitting someone square in the forehead.", "impaling someone's eye.", "disappearing.", "being hit by another paper plane.", "being sucked into another dimension.","flying out of the window.", "landing in a hornet's nest.", "hitting someone's face.", "being sucked into oblivion.", "was snatched out of the air by a cat and torn to shreds."]

sw_phrases = ["I find your lack of faith disturbing.", "When gone am I, the last of the Jedi will you be. The Force runs strong in your family. Pass on what you have learned.", "We must keep our faith in the Republic. The day we stop believing democracy can work is the day we lose it.", "I’m just a simple man trying to make my way in the universe.", "Fear is the path to the dark side. Fear leads to anger; anger leads to hate; hate leads to suffering. I sense much fear in you.", "Wars not make one great.", "Luminous beings are we…not this crude matter.", "Do or do not. There is no try.", "Power! Unlimited power!", "A Jedi uses the Force for knowledge and defense, never for attack.", "You have become what you swore to destroy!"]

colors = [0x7289da, 0xe67e22, 0x71368a, 0x9b59b6, 0x3498db, 0x1f8b4c, 0x11806a, 0x1abc9c,  0xc27c0e]

key_features = {
  'temp' : 'Temperature',
  'feels_like' : 'Feels Like (°C)',
  'temp_min' : 'Temp Min (°C)',
  'temp_max' : 'Temp Max (°C)',
  'humidity' : 'Humidity (%)',
  'pressure' : 'Pressure (hPa)',
  'sea_level': 'Sea Level (m)',
  'grnd_level': 'Ground level (m)'
}

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n" + " -" + json_data[0]['a']
    return (quote)

def direction(deg):
  if int(deg) == 0:
    return('North')
  elif int(deg) == 90:
    return('East')
  elif int(deg) == 180:
    return('South')
  elif int(deg) == 270:
    return('West')
  elif int(deg) > 0 and int(deg) < 90:
    return('Northeast')
  elif int(deg) > 90 and int(deg) < 180:
    return('Southeast')
  elif int(deg) > 180 and int(deg) < 270:
    return('Southwest')
  else:
    return('Northwest')

def content(c):
  if len(c) == 0:
    return('`The message was either an embed or an image. Text unavailable.`')
  else:
    return(c)

@client.event
async def on_message_edit(before, after):
  try:
    with open('edits.json', 'r') as f:
      m = json.load(f)
  
    m[str(before.guild.id)] = f'Before: {before.content}\nAfter: {after.content}\n{before.author.name} in #{before.channel.name}'

    with open('edits.json', 'w') as f:
      json.dump(m, f, indent=4)
  except:
    pass
    
@client.event
async def on_message_delete(message):
  try:
    with open('msgs.json', 'r') as f:
      m = json.load(f)
  
    m[str(message.guild.id)] = f'{message.author}: {message.content}\nChannel: #{message.channel.name}'

    with open('msgs.json', 'w') as f:
      json.dump(m, f, indent=4)
  except:
    pass


@client.event
async def on_guild_join(guild):
  file.insert_one({"_id": guild.id, "server_name": guild.name, "prefix": "i", "welcome_msg": 1})

@client.event
async def on_guild_remove(guild):
  file.delete_one({"_id":  guild.id})

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    pass
  else:
    pass

join_words = ['has joined this server!', 'is now a member of this server!', 'has hopped in to socialise!', 'just slid in!']

@client.event
async def on_member_join(member):
  listone = mydb["permaban"]
  listwo = listone.find()
  templist = []  
  for item in listwo:
    templist.append(item["_id"])
  if str(member.id) in templist:
    await member.kick(reason='Permanently banned')
    await member.send('You have been permanently banned from this server.')
  else:
    pass

  welcset = file.find_one({"_id": member.guild.id})["welcome_msg"]
  if welcset == 1:
    joinem = discord.Embed()
    joinem.title = f'{member} {random.choice(join_words)}'
    joinem.description = f'{member.name}, please remember to be nice!'
    joinem.color = random.choice(colors)
    joinem.set_thumbnail(url=member.avatar_url)
    await member.guild.system_channel.send(embed=joinem)
  elif welcset == 0:
    pass

def gavyn_weird_vids(message):
  bruh = message.attachments
  try:
    if str(bruh[0].content_type) == 'video/mp4' or str(bruh[0].content_type) == 'image/jpeg' or str(bruh[0].content_type) == 'image/png':
      return(1)
    else:
      return(0)
  except:
    return(0)

def gavyn_weird_embeds(message):
  try:
    a = message.embeds
    if len(a) != 0:
      return(1)
      
      try:
        print(a[0].to_dict())
      except:
        print('Fail lol')
    else:
      return(0)
  except:
    return(0)

async def banned_ppl():
  a = mydb["banned"]
  b = a.find()
  templist = []
  for item in b:
    templist.append(item["_id"])
  return(templist)

@client.event
async def on_reaction_add(reaction, user):
  blacklist = await banned_ppl()
  if reaction.emoji == '❎' and str(reaction.message.author.id) in blacklist and reaction.message.reactions[0].count > 1:
    message = reaction.message
    await message.delete()
    await message.channel.send('Please be reminded that usage of media must be kept civil. Please do not spam them or use them unnecessarily.')
    chan = await client.fetch_channel(877371559596158976)
    try:
      resend = message.attachments
      await chan.send(f'<@!{str(message.author.id)}>\n{resend[0].url}')
    except:
      await chan.send(f'<@!{str(message.author.id)}>\n{message.content}')
  else:
    pass


@client.event
async def on_message(message):
  await client.process_commands(message)
  blacklist = await banned_ppl()
  if str(message.author.id) in blacklist and message.channel.id != 877371559596158976:
    feedstocka = str(message.content.lower()) 
    feedstock = feedstocka[:17]
    if feedstock == 'https://tenor.com' or gavyn_weird_vids(message) == 1 or gavyn_weird_embeds(message) == 1:
      await message.add_reaction('❎')
    else:
      pass
    

@client.event
async def on_member_remove(member):
  welcset = file.find_one({"_id": member.guild.id})["welcome_msg"]
  if welcset == 1:
    joinem = discord.Embed()
    joinem.title = f'{member} has left the server'
    joinem.color = random.choice(colors)
    joinem.set_thumbnail(url=member.avatar_url)
    await member.guild.system_channel.send(embed=joinem)
  elif welcset == 0:
    pass

@client.event
async def on_ready():
    print('We are now logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'ihelp | In  {len(client.guilds)} servers!'))

async def listre(prev, channel):
  boc = requests.get(f'https://ll.thespacedevs.com/2.0.0/launch/{prev}/?mode=/?format=api').json()['results']
  em = discord.Embed()
  em.title=f'Giving an overview of 10 {prev} launches'
  em.color = random.choice(colors)
  for item in boc:
    status = item['status']['name']
    name = item['name']
    count = boc.index(item)+1
    if status == 'Go' or status == 'Success':
      em.add_field(name=f'{count}. {name}', value=f':green_circle: {status}', inline=False)
    elif status == 'TBD':
      em.add_field(name=f'{count}. {name}', value=f':yellow_circle: {status}', inline=False)
    else:
      em.add_field(name=f'{count}. {name}', value=f':red_circle: {status}', inline=False)
  await channel.send(embed=em)

async def ll(prev, ctx):
  boc = requests.get(f'https://ll.thespacedevs.com/2.0.0/launch/{prev}/?mode=/?format=api').json()['results']
  embeds = []
  
  for item in boc:
    boca = boc[boc.index(item)]
    em = discord.Embed()
    em.color = random.choice(colors)
    em.title=f'Showing info for the launch of {boca["name"]}'
    if boca["status"]["name"] == "Success":
      em.description=f'Status: {boca["status"]["name"]} :green_circle:'
    elif boca["status"]["name"] == "Failure":
      em.description=f'Status: {boca["status"]["name"]} :red_circle:'
    else:
      em.description=f'Status: {boca["status"]["name"]} :yellow_circle:'
    now = boca["window_start"]
    winstart = now.format("%A, %d %B %Y" + "\n"  "%H:%M:%S")
    winend = boca["window_end"].format("%d %B %Y" + "\n" + "%H:%M:%S")
    em.add_field(name='Time', value=f'{winstart} to {winend}', inline=False)
    em.add_field(name='Launch Service Provider', value=f'{boca["launch_service_provider"]["name"]} ({boca["launch_service_provider"]["type"]})', inline=False)
    em.add_field(name='Rocket', value=boca["rocket"]["configuration"]["full_name"], inline=False)
    em.add_field(name='Location', value=f'{boca["pad"]["name"]}\n[{boca["pad"]["location"]["name"]}]({boca["pad"]["map_url"]})', inline=False)
    em.add_field(name='Webcasted live?', value = boca["webcast_live"], inline=False)
    try:
      em.add_field(name=f'Mission ({boca["mission"]["type"]})', value=f'{boca["mission"]["description"][:500]}', inline=False)
    except:
      pass
    em.set_image(url=boca["pad"]["location"]["map_image"])
    if boca["image"] != None:
      em.set_thumbnail(url=boca["image"])
    embeds.append(em)
  await ctx.send(f'<@!{ctx.author.id}>')
  paginator = BotEmbedPaginator(ctx, embeds)
  await paginator.run()


def mass(item):
  if item == None:
    return('- ')
  else:
    return(item)

@client.command(aliases = ['ships'])
async def Ships(ctx):
    boc = requests.get('https://api.spacexdata.com/v4/ships').json()
    em = discord.Embed(title='Showing a list of SpaceX ships', description='These ships are primarily used for recovery missions to reuse Falcon boosters', color=random.choice(colors))
    em.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.ytimg.com%2Fvi%2Fr5bybH72JPo%2Fmaxresdefault.jpg&f=1&nofb=1')
    for item in boc:
      m = item["mass_kg"] 
      name = item["name"]
      count = boc.index(item)+1
      em.add_field(name=f'{count}. {name}', value=f'[Mass: {mass(m)}kg | Home port: {item["home_port"]} | Built in: {item["year_built"]}]({item["link"]})', inline=False)
    await ctx.reply(embed=em)

@client.command(aliases = ['capsules'])
async def Capsules(ctx):
  boc = requests.get('https://api.spacexdata.com/v4/capsules').json()
  em=discord.Embed(title='These capsules are spacecraft that have been designed and manufactured by SpaceX for a variety of purposes', description='Some are used for human transport while others are used to bring goods to the ISS', color=random.choice(colors))
  em.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F3%2F33%2FSpaceX_Crew_Dragon_(More_cropped).jpg%2F1200px-SpaceX_Crew_Dragon_(More_cropped).jpg&f=1&nofb=1')
  for item in boc:
    count = boc.index(item) + 1
    name = item["serial"]
    em.add_field(name=f'{count}. {name} | {item["type"]}', value=f'{item["last_update"]} ({item["status"]})', inline=False)
  await ctx.reply(embed=em)

def rocket_id(arg1):
  url = requests.get('https://api.spacexdata.com/v4/rockets').json()
  for item in url:
    if arg1.upper() == (item["name"]).upper():
      return(item["id"])
    else:
      pass

@client.command(aliases=['roadster'])
async def Roadster(ctx):
  url = requests.get('https://api.spacexdata.com/v4/roadster').json()
  em = discord.Embed(title=url["name"], description=url["details"], color=random.choice(colors))
  em.add_field(name='Launch Mass', value=f'{url["launch_mass_kg"]}kg', inline=False)
  em.add_field(name='Inclination', value=url["inclination"], inline=False)
  em.add_field(name='Speed', value=f'{url["speed_kph"]}km/h', inline=False)
  em.add_field(name='Distance from Earth', value=f'{url["earth_distance_km"]}km', inline=False)
  em.add_field(name='Distance from Mars', value=f'{url["mars_distance_km"]}km', inline=False)
  imgs = url["flickr_images"]
  templist = []
  for item in imgs:
    templist.append(item)
  em.set_image(url=random.choice(templist))
  await ctx.reply(embed=em)

@client.command(aliases=['rocket'])
async def Rocket(ctx, *, arg1):
  url = requests.get(f'https://api.spacexdata.com/v4/rockets/{rocket_id(arg1)}').json()
  em= discord.Embed(title=f'Showing data for {url["name"]}', description=url["description"], color=random.choice(colors))
  mass = url["mass"]["kg"]
  height = url["height"]["meters"]
  diameter = url["diameter"]["meters"]
  em.add_field(name='Height', value= f'{height}m', inline=False)
  em.add_field(name='Diameter', value= f'{diameter}m', inline=False)
  em.add_field(name='Mass', value= f'{mass}kg', inline=False)
  kone = url["second_stage"]["thrust"]["kN"]
  ktwo = url["second_stage"]["engines"]
  kthree = url["second_stage"]["burn_time_sec"]
  kfour = url["second_stage"]["fuel_amount_tons"]
  knone = url["first_stage"]["thrust_sea_level"]["kN"]
  kntwo = url["first_stage"]["thrust_vacuum"]["kN"]
  en = url["first_stage"]["engines"]
  bt = url["first_stage"]["burn_time_sec"]
  f = url["first_stage"]["fuel_amount_tons"]
  em.add_field(name='First stage stats', value=f'Thrust (Atmosphere): {knone}kN\nThrust (In space): {kntwo}kN\nEngines: {en}\nBurn time: {bt}s\nFuel required: {str(round(float(f)*907.185))}kg' , inline=False)
  em.add_field(name='Second stage stats', value=f'Thrust: {kone}kN\nEngines: {ktwo}\nBurn time: {kthree}s\nFuel required: {str(round(float(kfour)*907.185))}kg' , inline=False)
  em.add_field(name='Success rate', value=f'{url["success_rate_pct"]}%', inline=False)
  em.add_field(name='Cost per launch', value=f'{url["cost_per_launch"]}USD' , inline=False)
  em.set_image(url=url["flickr_images"][0])
  em.set_footer(text=f'Type {get_prefix(client, ctx.message)}rocket to get a list of all rockets!')
  await ctx.reply(embed=em)

@Rocket.error
async def Rocket_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply(f'Please specify a valid rocket name. Type `{get_prefix(client, ctx.message)}rocket` to get a list of SpaceX rockets.')
  elif isinstance(error, commands.MissingRequiredArgument):
    em = discord.Embed(title='Showing a list of SpaceX rockets', description='These rockets are manufactured and designed by SpaceX for human spaceflight and cargo missions.\nType `irocket <rocket name>` to get more stats.', color=random.choice(colors))
    url = requests.get('https://api.spacexdata.com/v4/rockets').json()
    for item in url:
      em.add_field(name=item["name"], value=item["description"], inline=False)
    await ctx.reply(embed=em)

@client.command(aliases = ['launch'])
async def Launch(ctx, arg1, prev):
  args = ['overview', 'previous', 'full', 'upcoming']
  if arg1 == 'overview':
    await listre(prev, ctx)
  elif arg1 == 'full':
    await ll(prev, ctx)
  if arg1 not in args or prev not in args:
    em = discord.Embed()
    em.color=random.choice(colors)
    em.title = 'Proper keywords for the launch feature'
    em.add_field(name='full/overview', value='Specifies whether you only want a list of launches or full data about each launch.', inline=False)
    em.add_field(name='previous/upcoming', value='Specifies whether you want data for previous or upcoming launches.', inline=False)
    em.add_field(name='Usage example', value=f'{get_prefix(client, ctx.message)}launch full upcoming', inline=False)
    await ctx.reply(embed=em)

@Launch.error
async def Launch_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    boc = requests.get('https://ll.thespacedevs.com/2.0.0/launch/previous/?mode=list/?format=api').json()
    await ctx.reply(boc["detail"])
  elif isinstance(error, commands.MissingRequiredArgument):
    em = discord.Embed()
    em.color=random.choice(colors)
    em.title = 'Proper keywords for the launch feature'
    em.add_field(name='full/overview', value='Specifies whether you want a list of launches or full data about each launch.', inline=False)
    em.add_field(name='previous/upcoming', value='Specifies whether you want data for previous or upcoming launches.', inline=False)
    em.add_field(name='Usage example', value=f'{get_prefix(client, ctx.message)}launch full upcoming', inline=False)
    await ctx.reply(embed=em)


@client.command(aliases = ['closures'])
async def Closures(ctx):
  boca = requests.get('https://api.bunnyslippers.dev/closures').json()[0]
  em=discord.Embed()
  em.title = 'Showing road closures for Starbase, TX'
  em.color=random.choice(colors)
  em.set_image(url='https://preview.redd.it/wfh5a6ovg7o81.jpg?width=960&crop=smart&auto=webp&s=3f846da242c2d025e73e6f0a3b5c22b0d7b77f82')
  for item in boca:
    em.add_field(name=item.upper(), value= boca[item], inline=False)
  await ctx.reply(embed=em)

def core_id(arg1):
  url = requests.get(f'https://api.spacexdata.com/v4/cores/').json()
  for item in url:
    if arg1 == item["serial"]:
      return(item["id"])
    else:
      pass
  
@client.command(aliases=['cores', 'Cores', 'booster'])
async def Booster(ctx, arg0):
  arg1 = arg0.upper()
  url = requests.get(f'https://api.spacexdata.com/v4/cores/{core_id(arg1)}').json()
  em= discord.Embed(title=f'Showing data for Falcon core {arg1}', description=url["last_update"], color=random.choice(colors))
  em.set_thumbnail(url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F8%2F83%2FCRS-18_Mission_(48380511427).jpg%2F1200px-CRS-18_Mission_(48380511427).jpg&f=1&nofb=1')
  em.add_field(name='Status', value=url["status"], inline=False)
  em.add_field(name='Reuse count', value=url["reuse_count"], inline=False)
  wenland = str(int(url["rtls_landings"]) + int(url["asds_landings"]))
  wenhop = str(int(url["rtls_attempts"]) + int(url["asds_attempts"]))
  em.add_field(name='Landings', value=f'{wenland}/{wenhop}', inline=False)
  em.add_field(name='No. of missions completed', value=len(url["launches"]), inline=False)
  await ctx.reply(embed=em)

@Booster.error
async def Booster_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply(f'Please specify a valid booster name.\nExample: {get_prefix(client, ctx.message)}booster B1059')
  else:
    await ctx.reply(f'Please specify the booster name after the command.\nExample: {get_prefix(client, ctx.message)}booster B1059')

@client.command(aliases=['invite'])
async def Invite(ctx):
  invite_embed=discord.Embed(title='Click the link and select the server you wish to invite me to.', description='https://discord.com/api/oauth2/authorize?client_id=849841146284736512&permissions=8&scope=bot', color=random.choice(colors))
  invite_embed.set_thumbnail(url=client.user.avatar_url)
  await ctx.reply(embed=invite_embed)

@client.command(aliases=['prefix'])
async def Prefix(ctx, prefix):
  file.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
  await ctx.reply(f'The prefix for this server has been changed to {prefix}')

@Prefix.error
async def Prefix_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please enter the new prefix after the command.\nExample: {get_prefix(client, ctx.message)}prefix *')

async def wolf_calc(term, formata):
  try:
    clienta = wolframalpha.Client('843APT-U7QXJJ8KET')
    try:
      response = clienta.query(term)
      a = next(response.results)
      b = a['subpod']['img'][formata]
      em = discord.Embed()
      em.title=term
      em.color=random.choice(colors)
      em.set_image(url=b)
      em.set_footer(text='Data provided by Wolfram Research, Inc.')
      return(em)
    except TypeError:
      response = clienta.query(term)
      a = next(response.results)
      b = a['subpod'][0]['img'][formata]
      em = discord.Embed()
      em.title=term
      em.color=random.choice(colors)
      em.set_image(url=b)
      em.set_footer(text='Data provided by Wolfram Research, Inc.')
      return(em)
  except RuntimeError:
      em = discord.Embed()
      em.title=term
      em.color=random.choice(colors)
      em.description="Wolfram Alpha's servers are unavailable. Please try again in 1 minute."
      em.set_footer(text='Data provided by Wolfram Research, Inc.')
      return(em)
      
@client.command(aliases=['calc', 'calculate'])
async def Calc(ctx, *, arg1):
  ans = await wolf_calc(arg1, '@src')
  await ctx.reply(embed=ans)

@Calc.error
async def Calc_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.reply(f'Please type your mathematical equation after the calc command.\nExample: {get_prefix(client, ctx.message)}calc 2^2 + x = 8')
    elif isinstance(error, commands.CommandInvokeError):
      await ctx.reply('The mathematical equation sent was invalid.')

@client.command(aliases=['server'])
async def Server(ctx):
  ID=ctx.message.guild.id
  name=ctx.message.guild.name
  server_embed=discord.Embed(title=f'Server Information for {name}', description=f'Server ID: {ID}', color=random.choice(colors))
  fetch = file.find_one({"_id": ctx.message.guild.id})
  def wlcm(dict):
    if dict["welcome_msg"] == 1:
      return('On')
    else:
      return('Off')
  server_embed.add_field(name='Bot Settings', value=f'Welcome Messages: {wlcm(fetch)}\nPrefix: {fetch["prefix"]}')
  server_embed.add_field(name='Member Count', value=ctx.message.guild.member_count, inline=False)
  server_embed.add_field(name='Server Name', value=ctx.message.guild.name, inline=False)
  server_embed.add_field(name='Owner', value=f'<@{ctx.message.guild.owner_id}>', inline=False)
  server_embed.add_field(name='Created On', value=ctx.message.guild.created_at.__format__("%A, %d %B %Y" + "\n"  "%H:%M:%S"), inline=False)
  server_embed.add_field(name='Maximum Members', value=ctx.message.guild.max_members, inline=False)
  server_embed.add_field(name='System Channel', value=ctx.message.guild.system_channel, inline=False)
  server_embed.add_field(name='Bitrate Limit', value=f'{ctx.message.guild.bitrate_limit}bps (bits/s)', inline=False)
  server_embed.add_field(name='Description', value=ctx.message.guild.description, inline=False)
  server_embed.add_field(name='Filesize Limit', value=f'{ctx.message.guild.filesize_limit}bytes', inline=False)
  server_embed.add_field(name='Total | Voice channels | Text Channels', value=f'{len(ctx.message.guild.channels)} | {len(ctx.message.guild.voice_channels)} | {len(ctx.message.guild.text_channels)}', inline=False)
  server_embed.set_thumbnail(url=ctx.message.guild.icon_url)
  await ctx.reply(embed=server_embed)

@client.command(aliases=['avatar'])
async def Avatar(ctx):
  member = ctx.message.mentions[0]
  img = member.avatar_url
  await ctx.reply(img)

@Avatar.error
async def Avatar_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply(ctx.author.avatar_url)

@client.command(aliases=['user'])
async def User(ctx):
  person = ctx.message.mentions[0]
  person_embed=discord.Embed(title=person.name, description=f'ID: {person.id}', color=random.choice(colors))
  person_embed.set_thumbnail(url=person.avatar_url)
  person_embed.add_field(name='Created on:', value=person.created_at.__format__('%A, %d %B %Y' + '\n' '%H:%M:%S'), inline=False)
  person_embed.add_field(name='Joined server on:', value=person.joined_at.__format__('%A, %d %B %Y' + '\n' '%H:%M:%S'), inline=False)
  try:
    person_embed.add_field(name='Server nickname:', value=person.nick, inline=False)
  except:
    person_embed.add_field(name='Server nickname:', value='None', inline=False)
  person_embed.add_field(name="Number of Roles:", value=len(person.roles), inline=False)
  person_embed.add_field(name="Bot?", value=person.bot, inline=False)
  await ctx.reply(embed=person_embed)

@User.error
async def User_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    person = ctx.author
    person_embed=discord.Embed(title=person.name, description=f'ID: {person.id}', color=random.choice(colors))
    person_embed.set_thumbnail(url=person.avatar_url)
    person_embed.add_field(name='Created on:', value=person.created_at.__format__('%A, %d %B %Y' + '\n' '%H:%M:%S'), inline=False)
    person_embed.add_field(name='Joined server on:', value=person.joined_at.__format__('%A, %d %B %Y' + '\n' '%H:%M:%S'), inline=False)
    try:
      person_embed.add_field(name='Server nickname:', value=ctx.author.nick, inline=False)
    except:
      person_embed.add_field(name='Server nickname:', value='None', inline=False)
    person_embed.add_field(name="Number of Roles:", value=len(person.roles), inline=False)
    person_embed.add_field(name="Bot?", value=person.bot, inline=False)
    await ctx.reply(embed=person_embed)
  else:
    await ctx.reply('The user mentioned is invalid.')

@client.command(aliases=['retrieve', 'snipe', 'Snipe'])
async def Retrieve(ctx):
  with open('msgs.json', 'r') as f:
    m = json.load(f)
  
  try:
    data = m[str(ctx.guild.id)]
  except:
    data = '-'

  with open('edits.json', 'r') as f:
    a = json.load(f)
  
  try:
    datatwo = a[str(ctx.guild.id)]
  except:
    datatwo = '-'
  em = discord.Embed()
  em.color=random.choice(colors)
  em.add_field(name='Last deleted message', value=data, inline=False)
  em.add_field(name='Last edited message', value=datatwo, inline=False)
  await ctx.reply(embed=em)

@client.command(aliases=['ping'])
async def Ping(ctx):
  ping_data=round(client.latency*1000)
  await ctx.reply('The latency is ' + f'`{ping_data}` ms.')

@client.command(aliases=['welcome'])
async def Welcome(ctx, arg1):
  if arg1 == 'on':
    file.update_one({"_id": ctx.guild.id}, {"$set": {"welcome_msg": 1}})
    await ctx.reply('Welcome messages for this server have been turned **on**.')
  elif arg1 == 'off':
    file.update_one({"_id": ctx.guild.id}, {"$set": {"welcome_msg": 0}})
    await ctx.reply('Welcome messages for this server have been turned **off**.')

@Welcome.error
async def Welcome_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify whether you want to turn welcome messages on or off.\nExample: {get_prefix(client, ctx.message)}welcome off')

@client.command(aliases=['clock'])
async def Clock(ctx, *, arg0):
  arg1 = arg0.replace(' ', '_')
  allt = pytz.all_timezones
  for item in allt:
    if item[-len(arg1):].lower() == arg1.lower():
      
      tz = pytz.timezone(item)
      
      datetime_8 = datetime.now(tz)
      zero8 = datetime_8.strftime("%m/%d/%Y\n%H:%M:%S")
      bruh = pytz.timezone("Etc/Universal")
      datetime_u = datetime.now(bruh)
      zerou = datetime_u.strftime("%H")
      gmt = int(datetime_8.strftime("%H")) - int(zerou)
      if gmt > 0:
        amt = str(f'+{gmt}')
      else:
        amt = str(gmt)
      em = discord.Embed(title=f'{item} [{amt}]', description=zero8, color=random.choice(colors))
      await ctx.reply(embed=em)
      return
    else:
      pass
  await ctx.reply(f'I could not find a town named {arg1} in the Orlan database.')
      
    
@Clock.error
async def clock_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    tz_0 = pytz.timezone('Etc/GMT+0')
    datetime_0 = datetime.now(tz_0)
    zero = datetime_0.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_4 = pytz.timezone('Etc/GMT-4')
    datetime_4 = datetime.now(tz_4)
    zero4 = datetime_4.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_8 = pytz.timezone('Etc/GMT-8')
    datetime_8 = datetime.now(tz_8)
    zero8 = datetime_8.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_12 = pytz.timezone('Etc/GMT-12')
    datetime_12 = datetime.now(tz_12)
    zero12 = datetime_12.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_n14 = pytz.timezone('Etc/GMT-14')
    datetime_n14 = datetime.now(tz_n14)
    zeron14 = datetime_n14.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_n10 = pytz.timezone('Etc/GMT+10')
    datetime_n10 = datetime.now(tz_n10)
    zeron10 = datetime_n10.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_n6 = pytz.timezone('Etc/GMT+6')
    datetime_n6 = datetime.now(tz_n6)
    zeron6 = datetime_n6.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_n2 = pytz.timezone('Etc/GMT+2')
    datetime_n2 = datetime.now(tz_n2)
    zeron2 = datetime_n2.strftime("%m/%d/%Y\n%H:%M:%S")
    tz_u = pytz.timezone('Etc/Universal')
    datetime_u = datetime.now(tz_u)
    zerou = datetime_u.strftime("%m/%d/%Y\n%H:%M:%S")
    clock = discord.Embed()
    clock.title = f'Showing different time zones worldwide'
    clock.description = f'Tip: Type {get_prefix(client, ctx.message)}clock <city name> to get the specific time of a city'
    clock.color = random.choice(colors)
    clock.add_field(name='GMT +0', value=zero, inline=True)
    clock.add_field(name='GMT +4', value=zero4, inline=True)
    clock.add_field(name='GMT +8', value=zero8, inline=True)
    clock.add_field(name='GMT +12', value=zero12, inline=True)
    clock.add_field(name='GMT +14', value=zeron14, inline=True)
    clock.add_field(name='GMT -10', value=zeron10, inline=True)
    clock.add_field(name='GMT -6', value=zeron6, inline=True)
    clock.add_field(name='GMT -2', value=zeron2, inline=True)
    clock.add_field(name='Universal', value=zerou, inline=True)
    clock.set_thumbnail(url='https://i.pinimg.com/originals/06/f4/52/06f4524b6efce7438442a91cb3e5a328.png')
    await ctx.reply(embed = clock)
  else:
    await ctx.reply('Congratulations, you have found an easter egg! Contact reverie3751025@gmail.com and provide him with [this code](https://www.youtube.com/watch?v=gfA-tPKPoNs) to receive your prize!')

@client.command(aliases=['fliptext'])
async def Fliptext(ctx, *, arg1):
  flipped = upsidedown.transform(arg1)
  await ctx.reply(flipped)

@Fliptext.error
async def Fliptext_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please write the text you want to flip after the fliptext command.\nExample: {get_prefix(client, ctx.message)}fliptext Can you come over later?')

@client.command(aliases=['reverse'])
async def Reverse(ctx, *, arg1):
   await ctx.reply(arg1[::-1])

@Reverse.error
async def Reverse_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please write the text you want to reverse after the reverse command.\nExample: {get_prefix(client, ctx.message)}reverse Have you heard about the recent SpaceX Starship launch?') 

@client.command(aliases=['clear'])
async def Clear(ctx, arg1):
  clear_number = int(arg1)
  try:
    async with ctx.channel.typing():
      deleted = await ctx.channel.purge(limit=clear_number)
      await ctx.send(f":broom: | <@!{ctx.author.id}> Deleted {len(deleted)} messages.")
  except discord.errors.Forbidden:
    await ctx.reply('No permissions to delete messages granted for Iridia.')
  except AttributeError:
    await ctx.reply('I cannot clear messsages in a DM channel')

@Clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the amount of messages you intend to delete after the clear command.\nExample: {get_prefix(client, ctx.message)}clear 2000')
  elif isinstance(error, commands.CommandInvokeError):
    await ctx.reply(f'Please specify the amount of messages you intend to delete after the clear command.\nExample: {get_prefix(client, ctx.message)}clear 2000')


@client.command(aliases=['timer'])
async def Timer(ctx, arg1, arg2):
  seconds = int(arg1)
  hours = str(arg2)
  if hours == 'm':
    await ctx.reply(f'⏱ | <@{ctx.author.id}> Timer set for {seconds} minutes!')
    await asyncio.sleep(seconds*60)
    await ctx.reply(f'⏱ | <@{ctx.author.id}> Timer is up!')
  elif hours == 'h':
    await ctx.reply(f'⏱ | <@{ctx.author.id}> Timer set for {seconds} hours!')
    await asyncio.sleep(seconds*3600)
    await ctx.reply(f'⏱ | <@{ctx.author.id}> Timer is up!')
  elif hours == 's' or hours == None:
    await ctx.reply(f'⏱ | <@{ctx.author.id}> Timer set for {seconds} seconds!')
    await asyncio.sleep(seconds)
    await ctx.reply(f'⏱ | <@{ctx.author.id}> Timer is up!')

@Timer.error
async def Timer_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Type how long you want the timer to be after the timer command (1 h, 1 s, 1m).\nExample: {get_prefix(client, ctx.message)}timer 2 s')
  else:
    await ctx.reply(f'Type how long you want the timer to be after the timer command (1 h, 1 s, 1m).\nExample: {get_prefix(client, ctx.message)}timer 4 h')

@client.command(aliases=['random'])
async def Random(ctx, arg1, arg2):
  min_number = int(arg1)
  max_number = int(arg2)
  await ctx.reply(random.randint(min_number, max_number))

@Random.error
async def Random_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Type the maximum and minimum numbers after the command.\nExample: {get_prefix(client, ctx.message)}random 200 2000')
  else:
    await ctx.reply(f'Type the maximum and minimum numbers after the command.\nExample: {get_prefix(client, ctx.message)}random 200 2000')

@client.command(aliases=['choose'])
async def Choose(ctx, *, arg1):
  choices = arg1.split(",")
  chosen = random.choice(choices)
  a = '\n'.join(choices)
  em = discord.Embed(title='__Options provided__', description = a, color=random.choice(colors))
  em.add_field(name='Chosen option', value=chosen, inline=False)
  await ctx.reply(embed=em)

@Choose.error
async def Choose_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the choices after the command. Separate them with commas.\nExample: {get_prefix(client, ctx.message)}choose Python,Javascript,C++')

@client.command(aliases=['vote', 'poll', 'Poll'])
async def Vote(ctx):
  voter = ctx.message.content.split(" ", 1)
  voting_text = voter[1]
  await ctx.channel.purge(limit=1)
  reacted = await ctx.send(f'**{voting_text}**')
  await reacted.add_reaction('✅')
  await reacted.add_reaction('❎')
  await asyncio.sleep(60)
  reacted = await reacted.channel.fetch_message(reacted.id)
  positive = 0
  negative = 0
  for reaction in reacted.reactions:
    if reaction.emoji == '✅':
      positive = reaction.count - 1 
    elif reaction.emoji == '❎':
      negative = reaction.count - 1
    
  if positive == negative:
      nes = discord.Embed(title=voting_text, description=f'Yes: {positive}' + '\n' + f'No: {negative}', color=random.choice(colors))
      nes.set_footer(text='The verdict is unknown! Call for another vote!')
      await ctx.send(embed=nes)
  elif positive > negative:
      yes = discord.Embed(title=voting_text, description=f'Yes: {positive}' + '\n' + f'No: {negative}', color=random.choice(colors))
      yes.set_footer(text='The verdict is yes!')
      await ctx.send(embed=yes)
  elif negative > positive:
      no = discord.Embed(title=voting_text, description=f'Yes: {positive}' + '\n' + f'No: {negative}', color=random.choice(colors))
      no.set_footer(text='The verdict is no!')
      await ctx.send(embed=no)

@Vote.error
async def Vote_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply(f'Please specify the poll topic after the vote command.\nExample: {get_prefix(client, ctx.message)}vote Is Python better than Javascript?')

@client.command(aliases=['plane'])
async def Plane(ctx):
  try:
    user = ctx.message.mentions[0]
    competitor = f'<@{user.id}>'
    comp_length = (random.randint(0, 700))
    user_length = (random.randint(0, 700))
    contest = await ctx.reply(f'✈ {competitor} and <@{ctx.message.author.id}> are throwing their paper planes...')
    await asyncio.sleep(random.randint(2,8))
    if comp_length > user_length:
      await contest.edit(content = f"{competitor}'s paper plane flew {comp_length}cm before " + random.choice(plane_words) + '\n' + f"<@{ctx.message.author.id}>'s plane flew {user_length}cm before " + random.choice(plane_words) + '\n' + f'{competitor} won!')
    else:
      await contest.edit(content = f"{competitor}'s paper plane flew {comp_length}cm before " + random.choice(plane_words) + '\n' + f"<@{ctx.message.author.id}>'s paper plane flew {user_length}cm before " + random.choice(plane_words) + '\n' + f'<@{ctx.message.author.id}> won!')
  except IndexError:
    flight_length=(random.randint(0, 700))
    paper = await ctx.reply('✈ Throwing paper plane...')
    await asyncio.sleep(random.randint(2, 6))
    await paper.edit(content = f"<@{ctx.message.author.id}>'s paper plane flew {flight_length}cm before " + random.choice(plane_words) + '\n' + "Come on, be a good sport and throw paper planes with someone else!")

@client.command(aliases=['ship'])
async def Ship(ctx, user3, user4):
  num = random.randint(1, 100)
  shipname = f'{user3[:round(len(user3)/2)]}{user4[-1*round(len(user4)/2):]}'
  em = discord.Embed()
  em.title=f'{user3} and {user4} 💖'    
  em.color=random.choice(colors)
  if num <= 20:
    em.description = f'[{shipname}]\n\n{num}% (Eww!)'
    await ctx.reply(embed = em)
  elif num >= 20 and num < 40:
    em.description = f'[{shipname}]\n\n{num}% (Not so great...)'
    await ctx.reply(embed = em)
  elif num >= 40 and num < 60:
    em.description = f'[{shipname}]\n\n{num}% (Ok, might do...)'
    await ctx.reply(embed = em)
  elif num >= 60 and num < 80:
    em.description = f'[{shipname}]\n\n{num}% (Pretty good!)'
    await ctx.reply(embed = em)
  elif num >= 80:
    em.description = f'[{shipname}]\n\n{num}% (Cute!)'
    await ctx.reply(embed = em)

@Ship.error
async def Ship_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please type the people you want to ship after the command.\nExample: {get_prefix(client, ctx.message)}ship Andrea Michael')

@client.command(aliases=['dice'])
async def Dice(ctx):
  dice_pics_1 = ['<:d6:806019379774226452>', '<:d5:810328229444452363>', '<:d4:806019355996979231>']
  dice_pics_2 = ['<:d3:810328197484118017>', '<:d2:806019324804333568>', '<:d1:810328161127497778>']
  roll = await ctx.reply('Rolling dice...' + '\n' + random.choice(dice_pics))
  for item in range(10):
    await asyncio.sleep(0.1)
    await roll.edit(content = 'Rolling dice...' + '\n' + random.choice(dice_pics_1))
    await asyncio.sleep(0.1)
    await roll.edit(content = 'Rolling dice...' + '\n' + random.choice(dice_pics_2)) 
  await roll.edit(content = 'You got:' + '\n' + random.choice(dice_pics))

@client.command(aliases=['meme'])
async def Meme(ctx):
  url="https://meme-api.herokuapp.com/gimme"
  meme = requests.get(url)
  json_meme = meme.json()
  postLink = json_meme["postLink"]
  subreddit = json_meme["subreddit"]
  title = json_meme["title"]
  author = json_meme["author"]
  ups = json_meme["ups"]
  url = json_meme["url"]

  meme_embed = discord.Embed(title=title, description=f"A funny meme from u/{author}", color=random.choice(colors))
  meme_embed.set_image(url=url)
  meme_embed.add_field(name="Upvotes", value=ups, inline=True)
  meme_embed.add_field(name="Subreddit", value=f"r/{subreddit}", inline=True)
  meme_embed.add_field(name="Link", value=f'[Click here]({postLink})')
  await ctx.reply(embed=meme_embed)

@client.command(aliases=['starwars'])
async def Starwars(ctx):
  await ctx.reply(random.choice(sw_phrases))

@client.command(aliases=['insult'])
async def Insult(ctx):
  person = ctx.message.mentions[0]
  url="https://insult.mattbas.org/api/en/insult.json"
  insult = requests.get(url)
  json_insult = insult.json()
  insult = json_insult["insult"]
  await ctx.reply(f"{person.name}, {insult.lower()}.")

@Insult.error
async def Insult_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    url="https://insult.mattbas.org/api/en/insult.json"
    insult = requests.get(url)
    json_insult = insult.json()
    insult = json_insult["insult"]
    await ctx.reply(f"{ctx.message.author.name}, {insult.lower()}.") 

@client.command(aliases=['flip'])
async def Flip(ctx):
  coin = await ctx.reply(':coin: Flipping coin...')
  await asyncio.sleep(random.randint(2,6))
  await coin.edit(content=random.choice(coin_words))

@client.command(aliases=['tragic'])
async def Tragic(ctx):
  user = ctx.message.mentions[0]
  usermention = user.name
  await ctx.reply(f'{usermention} ' + random.choice(tragic_events))

@Tragic.error
async def Tragic_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply(f'Please mention the name of the user you want to doom after the tragic command.\nExample: {get_prefix(client, ctx.message)}tragic @Lucy')

@client.command(aliases = ['8ball'])
async def eightball(ctx):
  await ctx.reply(random.choice(eightball_words))

@client.command(aliases = ['fact'])
async def Fact(ctx):
  animal = (random.choice(animal_words))
  url = f"https://some-random-api.ml/facts/{animal}"
  facts = requests.get(url)
  json_facts = facts.json()
  fact = json_facts["fact"]
  pic_url = f"https://some-random-api.ml/img/{animal}"
  pics = requests.get(pic_url)
  json_pics = pics.json()
  link = json_pics["link"]
      
  animal_embed=discord.Embed(title='I bet you never knew...', description=fact, color=random.choice(colors))
  animal_embed.set_image(url=link)
  await ctx.reply(embed=animal_embed)

@client.command(aliases=['covid'])
async def Covid(ctx, *, country=None):
  if country != None:
    thumburl = 'https://static.vecteezy.com/system/resources/thumbnails/000/834/835/original/coronavirus-background-in-futuristic-hud-style.jpg'
    url=f"https://coronavirus-19-api.herokuapp.com/countries/{country}"
    stats = requests.get(url)
    json_stats = stats.json()
    country = json_stats["country"]
    cases = json_stats["cases"]
    todayCases = json_stats["todayCases"]
    deaths = json_stats["deaths"]
    todayDeaths = json_stats["todayDeaths"]
    recovered = json_stats["recovered"]
    active = json_stats["active"]
    critical = json_stats["critical"]
    casesPerOneMillion = json_stats["casesPerOneMillion"]
    deathsPerOneMillion = json_stats["deathsPerOneMillion"]
    totalTests = json_stats["totalTests"]
    testsPerOneMillion = json_stats["testsPerOneMillion"]
    perc1 = (deaths/cases)*100
    perc2 = (recovered/cases)*100
    perc3 = (active/cases)*100
    perc1a = "{:.2f}".format(round(perc1, 2))
    perc1b = "{:.2f}".format(round(perc2, 2))
    perc1c = "{:.2f}".format(round(perc3, 2))
   
    covid_embed = discord.Embed(title=f"COVID-19 stats for {country}.",   description="Information may be slightly outdated.", color=random.choice(colors))
    covid_embed.set_footer(text="Social distance and wear a mask when you go out if you value lives.")
    covid_embed.set_thumbnail (url=thumburl)
    covid_embed.add_field(name="Total Cases", value=cases, inline=True)
    covid_embed.add_field(name="Today's Cases", value=todayCases, inline=True)
    covid_embed.add_field(name="Total Deaths", value=f'{deaths} ({perc1a}%)', inline=True)
    covid_embed.add_field(name="Today's Deaths", value=todayDeaths, inline=True)
    covid_embed.add_field(name="Recovered", value=f'{recovered} ({perc1b}%)', inline=True)
    covid_embed.add_field(name="Active", value=f'{active} ({perc1c}%)', inline=True)
    covid_embed.add_field(name="Critical", value=critical, inline=True)
    covid_embed.add_field(name="Total Tests", value=totalTests, inline=False)
    covid_embed.add_field(name="Cases /one million", value=casesPerOneMillion, inline=False)
    covid_embed.add_field(name="Deaths /one million", value=deathsPerOneMillion, inline=False)
    covid_embed.add_field(name="Tests /one million", value=testsPerOneMillion, inline=False)
    await ctx.reply(embed=covid_embed)
  elif country == None:
    pass
    await ctx.reply(f'Please specify the country you want stats for after the command.\nExample: {get_prefix(client, ctx.message)}covid Malaysia')

@Covid.error
async def Covid_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('Country not found in database.')

@client.command(aliases=['inspire'])
async def Inspire(ctx):
  quote = get_quote()
  await ctx.reply(quote)

@client.command(aliases=['weather'])
async def Weather(ctx, *, location):
  loca = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid=cd023bbe37a3aafd5fd85438f87cf6bd&units=metric').json()
  desc = loca['weather'][0]['description']
  con = loca['sys']['country']
  em=discord.Embed(title=f'Showing weather data for {loca["name"]} ({con})', description=f'Current situation: {desc}', color=random.choice(colors))
  for item in loca['main']:
    try:
      em.add_field(name=key_features[item], value=loca['main'][item], inline=True)
    except:
      pass
  long = loca['coord']['lon']
  lat = loca['coord']['lat']
  url = loca['weather'][0]['icon']
  windspeed = loca['wind']['speed']
  winddeg = loca['wind']['deg']
  direc = direction(winddeg)
  em.add_field(name='Coordinates', value=f'{long}, {lat}', inline=False)
  em.add_field(name='Wind', value=f'Wind speed: {windspeed}m/s\nDirection: {direc} ({winddeg}°)', inline=False)
  em.add_field(name='Visibility', value=loca['visibility'], inline=False)
  em.set_thumbnail(url=f'http://openweathermap.org/img/w/{url}.png')
  await ctx.reply(embed=em)

@Weather.error
async def Weather_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('City not found in database.')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the city you want data for after the weather command.\nExample: {get_prefix(client, ctx.message)}weather Kuching')

def synonyms(term):
  dic = requests.get(f"https://api.dictionaryapi.dev/api/v1/entries/en/{term}").json()[0]
  define = list(dic['meaning'])
  speech = define[0]
  defin = dic['meaning'][speech][0]['synonyms']
  if len(defin)>3:
    return(f'{defin[0]}, {defin[1]}, {defin[2]}')
  else:
    return(defin[0])

@client.command(aliases=['define', 'Dict', 'dict'])
async def Define(ctx, term):
    dic = requests.get(f"https://api.dictionaryapi.dev/api/v1/entries/en/{term}").json()[0]
    define = list(dic['meaning'])
    embeds = []
    for item in define:
      defin = str(dic['meaning'][item][0]['definition'])
      pro = dic['phonetics'][0]['text'] 
      proaud = dic['phonetics'][0]['audio'] 
      em = discord.Embed(title=f'{term} ({item})', description=f'{defin}\n[({pro})]({proaud})', color=random.choice(colors))
      em.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs0eH9KjEd77Ul5YWiII5Kli7C560JSYvBwg&usqp=CAU')
      try:
        em.add_field(name='Synonyms', value=synonyms(term), inline=False)
      except:
        pass
      try:
        exa = str(dic['meaning'][item][0]['example']) 
        em.add_field(name='Example', value=exa, inline=False)
      except:
        pass
      embeds.append(em)
    await ctx.send(f'<@!{ctx.author.id}>')
    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

@Define.error
async def Define_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('No definition was found for the word you were specifying.')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the word you definitions for.\nExample: {get_prefix(client, ctx.message)}Define coalesce')

@client.command(aliases=['urban'])
async def Urban(ctx, *, arg1):
  mainlist = requests.get(f"http://api.urbandictionary.com/v0/define?term={arg1}").json()["list"]
  embeds = []
  for dic in mainlist:
    perma = dic["permalink"]
    defin = dic["definition"]
    em = discord.Embed(title=f"Definition of the word {arg1}", description = f"{defin}", color=random.choice(colors))
    em.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fantisemitism.uk%2Fwp-content%2Fuploads%2F2020%2F02%2FUrban-Dictionary-1030x579.png&f=1&nofb=1")
    tu = dic["thumbs_up"]
    td = dic["thumbs_down"]
    if len(dic["example"]) != 0:
      em.add_field(name='Example', value=dic["example"], inline=False)
    else:
      pass
    em.add_field(name="Link", value=f"[Click here]({perma})", inline=False)
    d = dic["written_on"][:9]
    em.set_footer(text=f'Upload date: {d} by {dic["author"]}')
    embeds.append(em)

  await ctx.send(f'<@!{ctx.author.id}>')
  paginator = BotEmbedPaginator(ctx, embeds)
  await paginator.run()

@Urban.error
async def Urban_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('No definition was found for the word you were specifying.')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the word you definitions for.\nExample: {get_prefix(client, ctx.message)}urban Urban Dictionary')

@client.command(aliases=['orwell'])
async def Orwell(ctx):
  orwellian_pics = ["https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTgwNzU5NDU4MjAzMzEzNTEy/george-orwell.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/George_Orwell%2C_c._1940_%2841928180381%29.jpg/1200px-George_Orwell%2C_c._1940_%2841928180381%29.jpg", "https://images.theconversation.com/files/415532/original/file-20210810-27-1ph6862.jpg?ixlib=rb-1.1.0&rect=65%2C28%2C2617%2C1920&q=45&auto=format&w=926&fit=clip"]
  em = discord.Embed(title=random.choice(orwellian_quotes), description='- George Orwell', color=random.choice(colors))
  em.set_thumbnail(url=random.choice(orwellian_pics))
  await ctx.reply(embed=em)

async def google(arg1):
  def prettylink(link):
    if link[:4] != 'http':
      a = 'https:/' + link
      return(a)
    else:
      return(link)

  links = list(googlesearch.search(arg1, lang="en", num_results=4))
  
  url = links[0]
  res = requests.get(url)
  html_page = res.content
  soup = BeautifulSoup(html_page, 'html.parser')
  text = soup.find_all(text=True)

  output = ''
  blacklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']

  for t in text:
    if t.parent.name not in blacklist:
      output += '{} '.format(t)

  b = " ".join(output.split())

  shortie = b[:500]
  em = discord.Embed(title=arg1, description=f'{shortie}...\n{url}', color=random.choice(colors))
  em.add_field(name=f'Extra source no. 1', value=links[1], inline=False)
  em.add_field(name=f'Extra source no. 2', value=links[2], inline=False)
  em.set_footer(text='Data provided by Google LLC')
  return(em)

async def wikisearch_two(word): 
    page = wikipedia.page(word)
    content = str(page.content)
    desc = '%.1000s' % content
    link = page.url
    em = discord.Embed(title=page.title, description=f'{desc}...\n{link}', color=random.choice(colors))
    em.set_footer(text='Data provided by Wikipedia')
    try:
      pic = page.images
      pic1 = pic[0]
      em.set_image(url=pic1)
    except:
      pass
    return(em)

async def wikisearch(word): 
  try: 
    page = wikipedia.page(word)
    content = str(page.content)
    desc = '%.1000s' % content
    link = page.url
    em = discord.Embed(title=page.title, description=f'{desc}...\n{link}', color=random.choice(colors))
    em.set_footer(text='Data provided by Wikipedia')
    try:
      pic = page.images
      pic1 = pic[0]
      em.set_image(url=pic1)
    except:
      pass
    return(em, 1)
  except wikipedia.exceptions.DisambiguationError:
    content = wikipedia.search(word, results=5, suggestion=True)
    content1 = content[0]
    suggestions = discord.Embed()
    suggestions.title='Perhaps you meant'
    suggestions.description = 'Please type the name of the search term closest to your choice.'
    suggestions.color=random.choice(colors)
    suggestions.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvTZQhU67kQxuMVGC9NJBJlRsWq5-GOIAYYi4VBrfZ_DTuW6EbD9pPD9URxvDFMWSshkg&usqp=CAU')
    suggestions.set_footer(text='Data provided by Wikipedia')
    templist = []
    for item in content1:
      templist.append(item)
    for item in content1:
      try:
        suggestions.add_field(name=str(content1.index(item)+1), value=item, inline=False)
      except:
        pass
    return(suggestions, 0)

async def great_wolfram(term, formata):
  try:
    clienta = wolframalpha.Client('843APT-U7QXJJ8KET')
    try:
      response = clienta.query(term)
      a = next(response.results)
      b = a['subpod']['img'][formata]
      em = discord.Embed()
      em.title=term
      em.color=random.choice(colors)
      em.set_image(url=b)
      em.set_footer(text='Data provided by Wolfram Research, Inc.')
      return(em)
    except TypeError:
      response = clienta.query(term)
      a = next(response.results)
      b = a['subpod'][0]['img'][formata]
      em = discord.Embed()
      em.title=term
      em.color=random.choice(colors)
      em.set_image(url=b)
      em.set_footer(text='Data provided by Wolfram Research, Inc.')
      return(em)
  except RuntimeError:
      em = discord.Embed()
      em.title=term
      em.color=random.choice(colors)
      em.description="Wolfram Alpha's servers are unavailable. Please try again in 1 minute."
      em.set_footer(text='Data provided by Wolfram Research, Inc.')
      return(em)

@client.command(aliases=['search', 'wiki', 'google', 'query'])
async def Search(ctx, *, arg1):
  async with ctx.channel.typing():
      mothertext = await ctx.reply(f'<@{ctx.author.id}> Searching for answers...')
      embeds = []
      try:
        answerone = await great_wolfram(arg1, '@src')
        embeds.append(answerone)
      except:
        pass
      try:
        answertwo = await wikisearch_two(arg1)
        embeds.append(answertwo)
      except:
        pass
      try:
        answerthree = await google(arg1)
        embeds.append(answerthree)
      except:
        pass
      await mothertext.delete()

      if len(embeds) == 0:
        await ctx.reply('I could not find anything related to your query. Please try again with more specific keywords.')
        return
      else:
        pass

  await ctx.send(f'<@!{ctx.author.id}>')
  paginator = BotEmbedPaginator(ctx, embeds)
  await paginator.run()

@Search.error
async def Search_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the search term after the search command.\nExample: {get_prefix(client, ctx.message)}search y = 5x + 3')
  else:
    await ctx.reply('Something went wrong. Please try again :(')

def gptneo(payload, message):

  API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
  headers = {"Authorization": "Bearer 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"}
  data = json.dumps(payload)
  response = requests.request("POST", API_URL, headers=headers, data=data)
  t = response.json()
  s = t[0]['generated_text']
  return(f'{s}.')
  
@client.command(aliases=['prompt'])
async def Prompt(ctx, *, arg1):
  payload = {"inputs": arg1, "parameters":{"min_length": 5, "max_length": 300, "temperature": 0.85, "top_k": 20}}
  msg1 = await ctx.reply('Processing...')
  ans = gptneo(payload, ctx.message)
  await msg1.edit(content = ans)

@Prompt.error
async def Prompt_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please provide a prompt to generate text from.\nExample: {get_prefix(client, ctx.message)}Prompt Mike stared at the dark forest ahead in fear.')
  elif isinstance(error, commands.CommandInvokeError):
    await ctx.reply(':( Sorry, something went wrong. Please try again.')

@client.command(aliases=["updates"])
async def Updates(ctx):
  embedVar = discord.Embed(title="The Anew Update will be fully released soon!", description="New features and reworks will be shown here", color=random.choice(colors))
  embedVar.add_field(name="Added pagination for a few commands!", value=f"Urban dictionary, google dictionary, launches and more now show multiple results which you can access using :arrow_backward: or :arrow_forward:", inline=False)
  embedVar.add_field(name="Fixed the translation command", value="The bug causing the feature to fail when translating to English has been fixed.", inline=False)
  embedVar.add_field(name="Rolled Radia and Erin into Iridia", value="Music and AI NLP features are now added to Iridia.", inline=False)
  embedVar.add_field(name="Tidied up the help command", value="The help command now shows usage directions more clearly.", inline=False)
  embedVar.add_field(name="More stable hosting", value="Iridia will be migrated to Heroku and MongoDB, reducing outages and latency.", inline=False)
  embedVar.add_field(name="Small UI fixes and improvements", value="A few commands now have incremental but significant UI improvements.", inline=False)
  embedVar.set_thumbnail(url=client.user.avatar_url)
  await ctx.reply(embed=embedVar)

@client.command(aliases=['bot'])
async def Bot(ctx):
  botinfo = discord.Embed(title='Information about Iridia', description='A multipurpose bot for Discord users', color=random.choice(colors))
  lag = int(client.latency*1000)
  botinfo.add_field(name='Latency', value=f'{lag}ms', inline=False)
  botinfo.add_field(name='Number of servers', value=len(client.guilds), inline=False)
  botinfo.add_field(name='Number of users', value=len(client.users), inline=False)
  botinfo.add_field(name='Private channels', value=len(client.private_channels), inline=False)
  botinfo.add_field(name='ID', value=client.user.id, inline=False)
  botinfo.add_field(name='Birthday', value='17th December 2020', inline=False)
  botinfo.add_field(name='Python', value='v3.9')
  botinfo.add_field(name='Discord.py', value='v1.6.0')
  botinfo.set_thumbnail(url=client.user.avatar_url)
  await ctx.reply(embed=botinfo)

@client.command(aliases = ['kick'])
async def Kick(ctx, person: discord.Member, *, reason=None):
  kick_embed = discord.Embed(title=f'{person.name} has been kicked from this server.', description = f'Reason: {reason}', color=random.choice(colors)).set_thumbnail(url=person.avatar_url)
  await person.kick(reason=reason)
  await ctx.reply(embed=kick_embed)

@Kick.error
async def Kick_Error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the user you want to kick after the kick command and the reason(optional) for doing so.\nExample: {get_prefix(client, ctx.message)}kick @Andrea Spreading unverified information')
  elif isinstance(error, commands.MemberNotFound):
    await ctx.reply('I could not find the member you were specifying.')
  elif isinstance(error, commands.CommandInvokeError):
    await ctx.reply("I don't have permissions to kick this member!")

@client.command(aliases=['ban'])
async def Ban(ctx, person: discord.Member, *, reason=None):
  ban_embed = discord.Embed(title=f'{person.name} has been banned from this server.', description = f'Reason: {reason}', color=random.choice(colors)).set_thumbnail(url=person.avatar_url)
  await person.ban(reason=reason)
  await ctx.reply(embed=ban_embed)

@Ban.error
async def Ban_Error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the user you want to ban after the ban command and the reason for doing so.\nExample: {get_prefix(client, ctx.message)}ban @Andrea Sending NSFW images')
  elif isinstance(error, commands.MemberNotFound):
    await ctx.reply('I could not find the member you were specifying')
  else:
    await ctx.reply("No permissions granted to Iridia to ban this member.")

@client.command(aliases=['mediaban'])
async def Mediaban(ctx, person: discord.Member):
  blacklist = await banned_ppl()
  servers = [750273460177207396, 605009833199927296]
  if ctx.guild.id not in servers:
    await ctx.reply('This feature is not available in your server!')
    return
  elif str(ctx.author.id) in blacklist:
    await ctx.reply('You cannot use this feature when you are banned!')
    return
  elif person.id == client.user.id:
    await ctx.reply('You cannot use this feature against me.')
    return
  else:
    pass

  if str(person.id) not in blacklist:
    d = mydb["banned"]
    d.insert_one({"_id": str(person.id)})
    await ctx.reply(f'{person.name} is now banned from sending any videos and GIFs.')
  else:
    d.delete_one({"_id": str(person.id)})
    await ctx.reply(f'{person.name} has been unbanned from sending media')

@Mediaban.error
async def Mediaban_Error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the user you want to inflict this censorship on.\nExample: {get_prefix(client, ctx.message)}mediaban @Andrea')
  elif isinstance(error, commands.MemberNotFound):
    await ctx.reply('I could not find the member you were specifying')

@client.command(aliases=['permaban'])
async def Permaban(ctx, person: discord.Member, *, reason=None):
  g = mydb["permaban"]
  ban_embed = discord.Embed(title=f'{person.name} has been banned permanently from this server.', description = f'Reason: {reason}', color=random.choice(colors)).set_thumbnail(url=person.avatar_url)
  await person.ban(reason=reason)
  g.insert_one({"_id": str(person.id)})
  await ctx.reply(embed=ban_embed)

@Permaban.error
async def permaban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please specify the user you want to  permanently ban after the command and the reason for doing so.\nExample: {get_prefix(client, ctx.message)}permaban @Andrea Sending NSFW images')
  elif isinstance(error, commands.MemberNotFound):
    await ctx.reply('I could not find the member you were specifying')
  else:
    await ctx.reply("No permissions granted to Iridia to permanently ban this member.")

@client.command(aliases=['rename'])
async def Rename(ctx, member: discord.Member, *, nick):
  await member.edit(nick=nick)
  await ctx.reply(f'Nickname was changed for {member.name} to {nick}.')

@Rename.error
async def Rename_error(ctx, error):
  if isinstance(error, commands.MemberNotFound):
    await ctx.reply('I could not find that member.')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please mention the user you want to rename and the new nickname.\nExample: {get_prefix(client, ctx.message)}rename @Andrea Anna')
  elif isinstance(error, commands.CommandInvokeError):
    await ctx.reply('No permissions granted to Iridia to rename members.')

@client.command(aliases = ['roles'])
async def Roles(ctx, member: discord.Member):
  r = member.roles
  rolese = discord.Embed(title=f"Role info for {member}", description=f'Number of roles: {len(member.roles)}', color=random.choice(colors))
  rolese.set_thumbnail(url=member.avatar_url)
  for item in r:
    rolese.add_field(name=item, value=item.id, inline=False)
  await ctx.reply(embed=rolese)

@Roles.error
async def Roles_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    r = ctx.message.author.roles
    rolese = discord.Embed(title=f"Role info for {ctx.message.author}", description=f'Number of roles: {len(ctx.message.author.roles)}', color=random.choice(colors))
    rolese.set_thumbnail(url=ctx.message.author.avatar_url)
    for item in r:
      rolese.add_field(name=item, value=item.id, inline=False)
    await ctx.reply(embed=rolese)
  else:
    await ctx.reply('I could not find the member you were specifying!')

def prettytime(original):
  templist = original.split(":")
  a = len(templist)-1
  seconds = int(templist[a])
  if len(templist) == 2:
    templist.remove(templist[a])
    minutes = int(templist[0])
    b = seconds + (minutes*60)
    return(b)
  elif len(templist) == 3:
    templist.remove(templist[a])
    minutes = int(templist[1])
    hours = int(templist[0])
    c = seconds + (minutes*60) + (hours*3600)
    return(c)

async def addlist(guild_id, data):
  with open('songdict.json', 'r') as f:
    b = json.load(f)
  
  obj = b[guild_id]
  obj.append({"title": data["title"], "duration": data["duration"], "url": f'https://youtube.com{data["url_suffix"]}', "views": data["views"], "thumbnail": data["thumbnails"][0], "channel": data["channel"]})

  with open('songdict.json', 'w') as f:
    json.dump(b, f, indent=4)

  with open('songlist.json', 'r') as f:
    b = json.load(f)
  
  obj = b[guild_id]
  obj.append({"title": data["title"], "duration": data["duration"], "url": f'https://youtube.com{data["url_suffix"]}', "views": data["views"], "thumbnail": data["thumbnails"][0], "channel": data["channel"]})

  with open('songlist.json', 'w') as f:
    json.dump(b, f, indent=4)

async def tempremove(guild_id, data):
  with open('songlist.json', 'r') as f:
    b = json.load(f)
  
  obj = b[guild_id]
  obj.remove(data)

  with open('songlist.json', 'w') as f:
    json.dump(b, f, indent=4)

async def special_tempremove(guild_id, data):
  with open('songlist.json', 'r') as f:
    b = json.load(f)
  
  obj = b[guild_id]
  obj.remove({"title": data["title"], "duration": data["duration"], "url": f'https://youtube.com{data["url_suffix"]}', "views": data["views"], "thumbnail": data["thumbnails"][0], "channel": data["channel"]})

  with open('songlist.json', 'w') as f:
    json.dump(b, f, indent=4)

async def create(guild_id):
  with open('songdict.json', 'r') as f:
    b = json.load(f)
  
  b[guild_id] = []

  with open('songdict.json', 'w') as f:
    json.dump(b, f, indent=4)

  with open('songlist.json', 'r') as f:
    b = json.load(f)
  
  b[guild_id] = []

  with open('songlist.json', 'w') as f:
    json.dump(b, f, indent=4)

  with open('volume.json', 'r') as f:
    v = json.load(f)
  
  v[guild_id] = 100

  with open('volume.json', 'w') as f:
    json.dump(v, f, indent=4)

async def delete(guild_id):
  with open('songdict.json', 'r') as f:
    b = json.load(f)
  
  del b[guild_id]

  with open('songdict.json', 'w') as f:
    json.dump(b, f, indent=4)

  with open('songlist.json', 'r') as f:
    b = json.load(f)
  
  del b[guild_id]

  with open('songlist.json', 'w') as f:
    json.dump(b, f, indent=4)

  with open('volume.json', 'r') as f:
    v = json.load(f)
  
  del v[guild_id]

  with open('volume.json', 'w') as f:
    json.dump(v, f, indent=4)

async def pplay(ctx, data):
  voice = get(client.voice_clients, guild=ctx.guild)
  try:
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(data["url"], download=False)
      URL = link_check(info["url"], data["url"])
      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice.is_playing()
      views = data["views"]
      duration = data["duration"]
      chan = data["channel"]
      linkaaa = data["url"]
      em = discord.Embed(title=f' Now playing {data["title"]}', description=f"`Views:` {views}\n`Duration:` {duration}\n`Channel:` {chan}\n`Link:` {linkaaa}", color=random.choice(colors))
      em.set_thumbnail(url=data["thumbnail"])
      await ctx.send(embed=em)
      await asyncio.sleep(prettytime(duration))
      with open('songlist.json', 'r') as f:
        listener = json.load(f)
      try:
        await loopa(ctx, listener[str(ctx.guild.id)][0], voice)
        await tempremove(str(ctx.guild.id), data)
      except:
        pass
  except:
    if data["duration"] != None:
      pass
    else:
      await ctx.send(f'I could not retrieve the audio tracks for `{data["title"]}` :(')
      await tempremove(str(ctx.guild.id), data)
      pass
  
  def singertime(guild_id):
    with open('songlist.json', 'r') as f:
      listeners = json.load(f)
    return(listeners[guild_id])

  while len(singertime(str(ctx.guild.id))) != 0:
    for item in singertime(str(ctx.guild.id)):
      try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(item["url"], download=False)
          URL = link_check(info["url"], item["url"])
          voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
          voice.is_playing()
          views = item["views"]
          duration = item["duration"]
          chan = item["channel"]
          link_show = item["url"]
          em = discord.Embed(title=f'Now playing {item["title"]}', description=f"`Views:` {views}\n`Duration:` {duration}\n`Channel:` {chan}\n`Link:` {link_show}", color=random.choice(colors))
          em.set_thumbnail(url=item["thumbnail"])
          await ctx.send(embed=em)
          await asyncio.sleep(prettytime(duration))
          with open('songlist.json', 'r') as f:
            listener = json.load(f)
          try:
            await loopa(ctx, listener[str(ctx.guild.id)][0], voice)
            await tempremove(str(ctx.guild.id), item)
          except:
            pass
      except:
        if item["duration"] != None:
          return
        else:
          await ctx.send(f'I could not retrieve the audio tracks for `{item["title"]}` :(')
          await tempremove(str(ctx.guild.id), item)
          pass

loop_servers = []

async def loopa(ctx, data, voice):
  if str(ctx.guild.id) in loop_servers:
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(data["url"], download=False)
      URL = info['url']
      
      while str(ctx.guild.id) in loop_servers:
        audio = FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
        voice.play(audio)
        await asyncio.sleep(prettytime(data["duration"])+1)
  else:
    pass

def link_check(url, a_link):
  res = requests.get(url, stream=True)
  if res.status_code == 200:
    return(url)
  else:
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(a_link, download=False)
      final_link = info['url']
      return(final_link)
      
@client.command(aliases = ['j'])
async def join(ctx):
    await ctx.message.add_reaction('✅')
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
      await ctx.reply(f'Moved to channel {channel.name}')
    else:
      await channel.connect()
      await create(str(ctx.guild.id))
      await ctx.reply(f'Joined {channel.name}')

@join.error
async def join_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('Please join a channel first!')


@client.command(aliases = ['p'])
@commands.cooldown(1, 4, commands.BucketType.guild)
async def play(ctx, *, arg1):
  await ctx.message.add_reaction('🎧')
  voice = get(client.voice_clients, guild=ctx.guild)
  if not voice.is_playing():
    try:
      results = YoutubeSearch(arg1, max_results=10).to_dict()

      a = results[0]
    except:
      await ctx.reply('I could not find any tracks with the specified keywords.')
      return
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info(f'https://youtube.com{a["url_suffix"]}', download=False)
        URL = link_check(info["url"], f'https://youtube.com/{a["url_suffix"]}')
      except:
        await ctx.reply(f'I cannot play live videos. Please try again.')
        return
      voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      voice.is_playing()
      views = a["views"]
      duration = a["duration"]
      chan = a["channel"]
      link_show = f'https://youtube.com/{a["url_suffix"]}'
      em = discord.Embed(title=f'Now playing {a["title"]}', description=f"`Views:` {views}\n`Duration:` {duration}\n `Channel:` {chan}\n`Link:` {link_show}", color=random.choice(colors))
      em.set_thumbnail(url=a["thumbnails"][0])
      await ctx.reply(embed=em)
      await addlist(str(ctx.guild.id), a)
      await asyncio.sleep(prettytime(duration))
      with open('songlist.json', 'r') as f:
        listener = json.load(f)
      try:
        await loopa(ctx, listener[str(ctx.guild.id)][0], voice)
        await special_tempremove(str(ctx.guild.id), a)
      except:
        pass
      
      def singertime(guild_id):
        with open('songlist.json', 'r') as f:
          listeners = json.load(f)
        return(listeners[guild_id])

      while len(singertime(str(ctx.guild.id))) != 0:
        for item in singertime(str(ctx.guild.id)):
          with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
              info = ydl.extract_info(item["url"], download=False)
              URL = link_check(info["url"], item["url"])
              voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
              voice.is_playing()
              views = item["views"]
              duration = item["duration"]
              chan = item["channel"]
              link_show = item["url"]
              em = discord.Embed(title=f'Now playing {item["title"]}', description=f"`Views:` {views}\n`Duration:` {duration}\n`Channel:` {chan}\n`Link:` {link_show}", color=random.choice(colors))
              em.set_thumbnail(url=item["thumbnail"])
              await ctx.send(embed=em)
              await asyncio.sleep(prettytime(duration))
              with open('songlist.json', 'r') as f:
                listener = json.load(f)              
              try:
                await loopa(ctx, listener[str(ctx.guild.id)][0], voice)
                await tempremove(str(ctx.guild.id), item)
              except:
                pass
            except:
              if item["duration"] != None:
                return
              else:
                await ctx.reply(f'I could not retrieve the audio tracks for `{item["title"]}` :(')
                await tempremove(str(ctx.guild.id), item)
                pass
  else:
    try:
      results = YoutubeSearch(arg1, max_results=10).to_dict()

      a = results[0]
      if a["duration"] == '0':
        await ctx.reply('I cannot play live videos!')
        return
      else:
        await addlist(str(ctx.guild.id), a)
        em = discord.Embed(title=f'{a["title"]} has been added to the queue.', description=f'`Views:` {a["views"]}\n`Duration:` {a["duration"]}\n`Channel:` {a["channel"]}\n`Link:` https://youtube.com/{a["url_suffix"]}', color=random.choice(colors))
        em.set_thumbnail(url=a["thumbnails"][0])
        await ctx.reply(embed=em)
    except:
      await ctx.reply('I could not find an audio track with that keyword.')

@play.error
async def play_error(ctx, error):
  await ctx.message.add_reaction('🎧')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply(f'Add me to a voice channel by typing `{get_prefix(client, ctx.message)}join`.')
    raise error
  elif isinstance(error, commands.MissingRequiredArgument):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice == None:
      await ctx.reply(f'Add me to a voice channel by typing `{get_prefix(client, ctx.message)}join`.')
      return
    else:
      pass
    if voice.is_playing():
      await ctx.reply('Please specify the song you want me to play.')
      return
    else:
      pass
    with open('songdict.json', 'r') as f:
      b = json.load(f)
    playlist = b[str(ctx.guild.id)]
    if len(playlist) == 0:
      await ctx.reply('There is nothing in your playlist!')
    else:
      with open('songlist.json', 'r') as f:
        c = json.load(f)
      sl = c[str(ctx.guild.id)]
      for item in playlist:
        sl.append(item)
      
      with open('songlist.json', 'w') as f:
        json.dump(c, f, indent=4)

      await ctx.reply('I am now playing the queue.')
      await pplay(ctx, sl[0])
    
@client.command(aliases = ['le'])
async def leave(ctx):
  await ctx.message.add_reaction('✅')
  voice = get(client.voice_clients, guild=ctx.guild)

  if voice.is_playing():
    voice.stop()
  else:
    pass

  await ctx.guild.voice_client.disconnect() 
  await delete(str(ctx.guild.id))
  await create(str(ctx.guild.id))
  await ctx.reply(f'Disconnected from the voice channel.')

@leave.error
async def leave_error(ctx, error):
  await ctx.message.add_reaction('✅')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('I am not in a voice channel!')

@client.command()
@commands.cooldown(1, 2, commands.BucketType.guild)
async def skip(ctx):
  await ctx.message.add_reaction('⏭️')
  with open('songdict.json', 'r') as f:
    b = json.load(f)
  a = b[str(ctx.guild.id)]

  with open('songlist.json', 'r') as f:
    d = json.load(f)
  c = d[str(ctx.guild.id)]

  if len(a) == 1:
    await ctx.reply('You cannot skip to the next track.')
  elif len(c) <= 1:
    await ctx.reply('You are already playing the last track of the queue.')
  else:
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    with open('songlist.json', 'r') as f:
      d = json.load(f)
    c = d[str(ctx.guild.id)]
    e = c[1]
    v = c[0]
    voice.stop()
    await tempremove(str(ctx.guild.id), v)
    await asyncio.sleep(0.5)
    await ctx.reply(f'Skipped from `{v["title"]}` to `{e["title"]}`.')
    await pplay(ctx, e)

@skip.error
async def skip_error(ctx, error):
  await ctx.message.add_reaction('⏭️')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You are not playing anything!')
  
@client.command(aliases = ['q'])
async def queue(ctx):
  await ctx.message.add_reaction('📑')
  voice = get(client.voice_clients, guild=ctx.guild)
  with open('songdict.json', 'r') as f:
    a = json.load(f)
  b = a[str(ctx.guild.id)]
  em = discord.Embed()
  em.title = 'Showing the queue for this server'

  if voice.is_playing():
    with open('songlist.json', 'r') as f:
      d = json.load(f)
    asdf = d[str(ctx.guild.id)]
    asd = d[str(ctx.guild.id)][0]["title"]
    p = len(b) - len(asdf)
    em.description = f'Now playing: `{asd}`\nSongs completed: {p}/{len(b)}'
  else:
    pass

  em.color=random.choice(colors)
  for item in b:
    em.add_field(name=f'{b.index(item)+1}. {item["title"]}', value=item["duration"], inline=False)
  await ctx.reply(embed=em)

@queue.error
async def queue_error(ctx, error):
  await ctx.message.add_reaction('📑')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You are currently not playing anything.')

@client.command(aliases = ['rem'])
async def remove(ctx, arg1):
  await ctx.message.add_reaction('🗑️')
  voice = get(client.voice_clients, guild=ctx.guild)
  with open('songdict.json', 'r') as f:
    b = json.load(f)
  
  obj = b[str(ctx.guild.id)]
  try:
    song = obj[int(arg1)-1]
    obj.pop(int(arg1)-1)
  except IndexError:
    await ctx.reply('The song you are trying to remove is not in the queue!')
    return 

  with open('songdict.json', 'w') as f:
    json.dump(b, f, indent=4)
  with open('songlist.json', 'r') as f:
    c = json.load(f)
  
  bruh = c[str(ctx.guild.id)]
  if len(bruh) == 0:
    try:
      bruh.remove(song)
    except:
      pass

    with open('songlist.json', 'w') as f:
      json.dump(c, f, indent=4)
    await ctx.reply(f'`{song["title"]}` has been removed from the queue.')
  else:
    if bruh[0]["url"] == song["url"]:
      if len(bruh) <= 1:
        voice.stop()
        try:
          bruh.remove(song)
        except:
          pass

        with open('songlist.json', 'w') as f:
          json.dump(c, f, indent=4)
        await ctx.reply(f'`{song["title"]}` has been removed from the queue.')
      else:
        newsong = bruh[1]
        voice.stop()
        try:
          bruh.remove(song)
        except:
          pass

        with open('songlist.json', 'w') as f:
          json.dump(c, f, indent=4)
        await ctx.reply(f'`{song["title"]}` has been removed from the queue.')
        await pplay(ctx, newsong)
    else:
      try:
        bruh.remove(song)
      except:
        pass

      with open('songlist.json', 'w') as f:
        json.dump(c, f, indent=4)
      await ctx.reply(f'`{song["title"]}` has been removed from the queue.')

@remove.error
async def remove_error(ctx, error):
  await ctx.message.add_reaction('🗑️')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You do not have any songs in your queue!')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply('Please specify the index of the song you intend to delete.\nExample: `r.remove 2`')

@client.command()
async def loop(ctx):
  await ctx.message.add_reaction('🔁')
  voice = get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    if str(ctx.guild.id) not in loop_servers:
      with open('songlist.json', 'r') as f:
        d = json.load(f)
      a = d[str(ctx.guild.id)]
      loop_servers.append(str(ctx.guild.id))
      await ctx.reply(f'Now looping `{a[0]["title"]}.`')
    else:
      loop_servers.remove(str(ctx.guild.id))
      with open('songlist.json', 'r') as f:
        d = json.load(f)
      a = d[str(ctx.guild.id)]
      await ctx.reply(f'`{a[0]["title"]}` has been unlooped.')
  else:
    await ctx.reply('You are currently not playing anything.')

@loop.error
async def loop_error(ctx, error):
  await ctx.message.add_reaction('🔁')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You are currently not playing anything.')

@client.command()
async def empty(ctx):
  await ctx.message.add_reaction('✅')
  voice = get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.stop()
  else:
    pass
  await delete(str(ctx.guild.id))
  await create(str(ctx.guild.id))
  await ctx.reply('The queue for this server has been cleared.')

@empty.error
async def empty_error(ctx, error):
  await ctx.message.add_reaction('✅')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You have not played any tracks!')
  
@client.command(aliases = ['res'])
async def resume(ctx):
  await ctx.message.add_reaction('▶️')
  voice = get(client.voice_clients, guild=ctx.guild)

  if not voice.is_playing():
    with open('songlist.json', 'r') as f:
      d = json.load(f)
    song = d[str(ctx.guild.id)][0]["title"]
    voice.resume()
    await ctx.reply(f'`{song}` has been resumed.')
  else:
    await ctx.reply('You are currently not pausing any track.')

@resume.error
async def resume_error(ctx, error):
  await ctx.message.add_reaction('▶️')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You are currently not playing anything!')

@client.command(aliases = ['pa'])
async def pause(ctx):
  await ctx.message.add_reaction('⏸️')
  voice = get(client.voice_clients, guild=ctx.guild)

  if voice.is_playing():
    with open('songlist.json', 'r') as f:
      d = json.load(f)
    song = d[str(ctx.guild.id)][0]["title"]
    voice.pause()
    await ctx.reply(f'`{song}` has been paused.')
  else:
    await ctx.reply('You currently have a track paused.')

@pause.error
async def pause_error(ctx, error):
  await ctx.message.add_reaction('⏸️')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You are currently not playing anything!')

extract_lyrics = SongLyrics('AIzaSyCan0eMVlKM2ufB9fzpM8etVUJKh_IYJGg', '47df21fd6a119f6f3')

@client.command(aliases=['ly'])
@commands.cooldown(1, 2, commands.BucketType.user)
async def lyrics(ctx, *, song):
  await ctx.message.add_reaction('🎶')
  data = extract_lyrics.get_lyrics(song)
  lys = data['lyrics']
  info = (lys[:2045] + '..') if len(lys) > 2048 else lys
  lytitle = data['title']
  lyem = discord.Embed(title=lytitle, description=info, color=random.choice(colors))
  await ctx.reply(embed=lyem)

@lyrics.error
async def lyrics_error(ctx, error):
  await ctx.message.add_reaction('🎶')
  if isinstance(error, commands.MissingRequiredArgument):
    try:
      with open('songlist.json', 'r') as f:
        b = json.load(f)
      a = b[str(ctx.guild.id)][0]
      try: 
        song = a["title"]
        data = extract_lyrics.get_lyrics(song)
        lys = data['lyrics']
        info = (lys[:2045] + '..') if len(lys) > 2048 else lys
        lytitle = data['title']
        lyem = discord.Embed(title=f'Lyrics for {lytitle}', description=info, color=random.choice(colors))
        lyem.set_thumbnail(url=a["thumbnail"])
        await ctx.reply(embed=lyem)
      except:
        await ctx.reply(f'I cannot find lyrics for {song.name}.')
    except:
      await ctx.reply('Please play a song or specify the name of the song you want lyrics for.')
  elif isinstance(error, commands.CommandInvokeError):
    await ctx.reply('I cannot find lyrics for the song you have specified.')

@client.command()
async def np(ctx):
  await ctx.message.add_reaction('🎙️')
  with open('songlist.json', 'r') as f:
    b = json.load(f)
  a = b[str(ctx.guild.id)][0]

  em = discord.Embed(title=f'Currently playing {a["title"]}', description=f'`Duration:` {a["duration"]}\n`Views:` {a["views"]}\n`URL:` [Click here]({a["url"]})', color=random.choice(colors))
  em.set_thumbnail(url=a["thumbnail"])
  await ctx.reply(embed=em)

@np.error
async def np_error(ctx, error):
  await ctx.message.add_reaction('🎙️')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You are currently not playing anything!')

@client.command(aliases=['v'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def volume(ctx, arg1):
  
  await ctx.message.add_reaction('🔊')
  voice = get(client.voice_clients, guild=ctx.guild) 
  if float(arg1) > 0 and float(arg1) < 20000:                          
    if voice.is_playing():      
      with open('volume.json', 'r') as f:
        c = json.load(f)
      a = c[str(ctx.guild.id)]   

      new_volume = float(arg1) / a           
      voice.source = discord.PCMVolumeTransformer(voice.source)
      
      voice.source.volume = new_volume 
      
      c[str(ctx.guild.id)] = float(arg1)

      with open('volume.json', 'w') as f:
        json.dump(c, f, indent=4)

      await ctx.reply(f'Volume has been changed to `{arg1}`')       
    else:                                           
      await ctx.reply(f"You are not playing anything!")   
  else:                                               
    await ctx.reply("Please specify an integer from 1 to 100!")

@volume.error
async def volume_error(ctx, error):
  await ctx.message.add_reaction('🔊')
  if isinstance(error, commands.CommandInvokeError):
    await ctx.reply('You can only change the volume when I am playing an audio track!')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply('Please specify the volume you want me to apply!')

@client.command()
async def competitivanfuture(ctx):
  await ctx.reply('You have found an Easter egg! Contact `reverie3751025@gmail.com` and provide him with this video to claim your prize!\nhttps://www.youtube.com/watch?v=gfA-tPKPoNs')

@client.command()
async def playlist(ctx, arg1, *, arg2):
  await ctx.message.add_reaction('🎶')
  musica = mydb["music_service"]
  try:
    yeno = musica.find_one({"_id": ctx.author.id})
  except:
    musica.insert_one({"_id": ctx.author.id, "info": []})
  if arg1 == 'add' and yeno == None:
    try:
      results = YoutubeSearch(arg2, max_results=10).to_dict()
      a = results[0]
    except:
      await ctx.reply('I could not find any tracks with the specified keywords.')
      return
    musica.insert_one({"_id": ctx.author.id, "info": [{"title": a["title"], "duration": a["duration"], "url": f'https://youtube.com{a["url_suffix"]}', "views": a["views"], "thumbnail": a["thumbnails"][0], "channel": a["channel"]}]})
  elif arg1 == 'add' and yeno != None:
    musiclist = yeno['info']
    try:
      results = YoutubeSearch(arg2, max_results=10).to_dict()
      a = results[0]
    except:
      await ctx.reply('I could not find any tracks with the specified keywords.')
      return
    musiclist.append({"title": a["title"], "duration": a["duration"], "url": f'https://youtube.com{a["url_suffix"]}', "views": a["views"], "thumbnail": a["thumbnails"][0], "channel": a["channel"]})
    musica.update_one({"_id": ctx.author.id}, {"$set": {"info": musiclist}})
    await ctx.reply(f'{a["title"]} has been added to your personal playlist.')
  elif arg1 == 'remove':
    musiclist = yeno["info"]
    bruh = yeno['info'][int(arg2)-1]['title']
    musiclist.pop(int(arg2)-1)
    musica.update_one({"_id": ctx.author.id}, {"$set":{"info": musiclist}})
    await ctx.reply(f'{bruh} has been removed from your personal playlist.')
    
@playlist.error
async def playlist_error(ctx, error):
  await ctx.message.add_reaction('🎶')
  musica = mydb["music_service"]
  if isinstance(error, commands.MissingRequiredArgument):
    if ctx.message.content.startswith(f'{get_prefix(client, ctx.message)}playlist play') == True or ctx.message.content.startswith(f'{get_prefix(client, ctx.message)}playlist view') == True:
      if ctx.message.content.startswith(f'{get_prefix(client, ctx.message)}playlist view'):
        yeno = musica.find_one({"_id": ctx.author.id})
        muselist = yeno["info"]
        em = discord.Embed(title=f"{ctx.author.name}'s playlist", description=f'`{len(muselist)} tracks added`', color=random.choice(colors))
        for item in muselist:
          em.add_field(name=f'{muselist.index(item)+1}. {item["title"]}', value=item["channel"], inline=False)
        await ctx.reply(embed=em)
      elif ctx.message.content.startswith(f'{get_prefix(client, ctx.message)}playlist play'):
        yeno = musica.find_one({"_id": ctx.author.id})
        muselist = yeno["info"]
        if len(muselist) < 1:
          await ctx.reply('You do not have any songs in your personal playlist!')
          return
        else:
          pass
        song = yeno["info"][0]
        with open('songdict.json', 'r') as f:
          v = json.load(f)

        with open('songlist.json', 'r') as f:
          d = json.load(f)

        if len(v[str(ctx.guild.id)]) > 0:
          for item in muselist:
            v[str(ctx.guild.id)].append(item)
            d[str(ctx.guild.id)].append(item)
          with open('songdict.json', 'w') as f:
            json.dump(v, f, indent=4)

          with open('songlist.json', 'w') as f:
            json.dump(d, f, indent=4)
          await ctx.reply('Added songs to the server playlist.')
        else:
          voice = get(client.voice_clients, guild=ctx.guild)
          if voice == None:
            try:
              channel = ctx.message.author.voice.channel
              await channel.connect()
              await ctx.reply(f'Joined {channel.name}')
            except:
              await ctx.reply('Please join a voice channel first!')
              return
          await create(str(ctx.guild.id))
          with open('songdict.json', 'r') as f:
            v = json.load(f)

          with open('songlist.json', 'r') as f:
            d = json.load(f)
            
          for item in muselist:
            v[str(ctx.guild.id)].append(item)
            d[str(ctx.guild.id)].append(item)

          with open('songdict.json', 'w') as f:
            json.dump(v, f, indent=4)

          with open('songlist.json', 'w') as f:
            json.dump(d, f, indent=4)

          await ctx.reply('Now playing your playlist.')
          await pplay(ctx, song)
      else:
        await ctx.reply(f'Please specify the required arguments! (Examples below)\n`{get_prefix(client, ctx.message)}playlist add never gonna give you up`\n`{get_prefix(client, ctx.message)}playlist remove 3`\n`{get_prefix(client, ctx.message)}playlist play`\n`{get_prefix(client, ctx.message)}playlist view`')
    else:
      await ctx.reply(f'Please specify the required arguments! (Examples below)\n`{get_prefix(client, ctx.message)}playlist add never gonna give you up`\n`{get_prefix(client, ctx.message)}playlist remove 3`\n`{get_prefix(client, ctx.message)}playlist play`\n`{get_prefix(client, ctx.message)}playlist view`')
  else:
    await ctx.reply('Something went wrong. Please try again.')


@client.command(aliases=["command", "help", "Command"])
async def Help(ctx):
  mynum = await client.fetch_user(746646972483502140)
  mypic = mynum.avatar_url
  myname = mynum.name

  embed1 = discord.Embed(title="Command List Categories", description="A list of commands to talk to Iridia!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name="Prefix", value='i', inline=False).add_field(name='Server prefix', value=get_prefix(client, ctx.message), inline=False).add_field(name="Jokes/Fun", value="`pg 2`", inline=False).add_field(name="Tools", value="`pg 3`", inline=False).add_field(name="Productivity", value="`pg 4`", inline=False).add_field(name="Mod/Server", value="`pg 5`", inline=False).add_field(name="Bot", value="`pg 6`", inline=False).add_field(name="SpaceX", value="`pg 7`", inline=False).add_field(name="Music Commands 1", value="`pg 8`", inline=False).add_field(name="Music Commands 2", value="`pg 9`", inline=False)

  embed2 = discord.Embed(title="Fun-themed Commands", description="A list of commands to talk have some fun with Iridia!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name="Get insulted", value=f"`{get_prefix(client, ctx.message)}insult`", inline=False).add_field(name="Get a meme", value=f"`{get_prefix(client, ctx.message)}meme`", inline=False).add_field(name="Get a Star Wars line", value=f"`{get_prefix(client, ctx.message)}starwars`", inline=False).add_field(name="Shipping Service", value=f"`{get_prefix(client, ctx.message)}ship`", inline=False).add_field(name="Roll a dice", value=f'`{get_prefix(client, ctx.message)}dice`', inline=False).add_field(name="Throw a paper plane with friend or by yourself", value=f"`{get_prefix(client, ctx.message)}plane` or `{get_prefix(client, ctx.message)}plane <@someone>`").add_field(name="Doom a friend or enemy", value=f'`{get_prefix(client, ctx.message)}tragic` or `{get_prefix(client, ctx.message)}tragic <@someone>`', inline=False).add_field(name="Get facts about animals", value=f"`{get_prefix(client, ctx.message)}fact`", inline=False).add_field(name="Flip messages", value=f'`{get_prefix(client, ctx.message)}fliptext <text>`', inline=False).add_field(name="Reverse text", value=f'`{get_prefix(client, ctx.message)}reverse <text>`', inline=False).add_field(name="Get Urban Dictionary definitions", value=f'`{get_prefix(client, ctx.message)}urban <word>`', inline=False)

  embed3 = discord.Embed(title="Commands to access tools", description="Access essential tools with these commands!", color=random.choice(colors)).set_thumbnail(url=client.user.avatar_url).set_footer(icon_url=mypic, text=f'Bot created by {myname}').add_field(name="Ask the 8ball", value=f"`{get_prefix(client, ctx.message)}8ball`", inline=False).add_field(name="Flip a coin", value=f"`{get_prefix(client, ctx.message)}flip`", inline=False).add_field(name="Get a random number between 0 and a specified positive integer.", value=f"`{get_prefix(client, ctx.message)}random <min> <max>`", inline=False).add_field(name="Create a minute long poll in the chat", value=f"`{get_prefix(client, ctx.message)}vote <poll topic>`", inline=False).add_field(name="See your avatar or someone else's", value=f"`{get_prefix(client, ctx.message)}avatar <@someone>` or `{get_prefix(client, ctx.message)}avatar`", inline=False).add_field(name="Let Iridia choose something from a range of options", value=f"`{get_prefix(client, ctx.message)}choose <option1>,<option2>...`", inline=False).add_field(name="Find out how high the latency is", value=f"`{get_prefix(client, ctx.message)}ping`", inline=False).add_field(name="Get current time around the world", value=f'`{get_prefix(client, ctx.message)}clock` or `{get_prefix(client, ctx.message)}clock <city name>`', inline=False).add_field(name="Generate a story with AI and Natural Language Processing", value=f'`{get_prefix(client, ctx.message)}prompt <text>`', inline=False)

  embed4 = discord.Embed(title="Commands to access productivity features", description="Be productive with these commands!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name="View COVID-19 cases around the globe", value=f"`{get_prefix(client, ctx.message)}covid <country name>`", inline=False).add_field(name="Search for some information from the internet", value=f"`{get_prefix(client, ctx.message)}search <query>`", inline=False).add_field(name="Inspirational Quotes", value=f"`{get_prefix(client, ctx.message)}inspire`", inline=False).add_field(name="Get weather stats for a specific place", value=f"`{get_prefix(client, ctx.message)}weather <name of place>`", inline=False).add_field(name='Translate text to a specified language', value=f'`{get_prefix(client, ctx.message)}translate <language> <text to translate>`', inline=False).add_field(name="Set a timer", value=f"`{get_prefix(client, ctx.message)}timer <number> <time unit>`", inline=False).add_field(name="Calculator", value=f"`{get_prefix(client, ctx.message)}calc <maths equation>`", inline=False).add_field(name="Dictionary", value=f"`{get_prefix(client, ctx.message)}define <word>`", inline=False).add_field(name='Get an Orwellian quote', value=f'`{get_prefix(client, ctx.message)}orwell`', inline=False)
  
  embed7 = discord.Embed(title="Commands to access bot info", description="Know bot information with these commands!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name="Default prefix", value='i', inline=False).add_field(name="Get an invite link for Iridia", value=f"`{get_prefix(client, ctx.message)}invite`", inline=False).add_field(name="View recent updates", value=f"`{get_prefix(client, ctx.message)}updates`", inline=False).add_field(name="View bot info", value=f"`{get_prefix(client, ctx.message)}bot`", inline=False)

  embed5 = discord.Embed(title="Server/mod commands for Iridia", description="Get important mod-based information and features with Iridia!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name="Ban members", value=f"`{get_prefix(client, ctx.message)}ban <@someone> <reason>`", inline=False).add_field(name="Kick members", value=f"`{get_prefix(client, ctx.message)}kick <@someone> <reason>`", inline=False).add_field(name="Get server information", value=f"`{get_prefix(client, ctx.message)}server`", inline=False).add_field(name="Clear Messages", value=f"`{get_prefix(client, ctx.message)}clear <amt of messages>`", inline=False).add_field(name="Get stats for your discord account or someone else's", value=f"`{get_prefix(client, ctx.message)}user` or `{get_prefix(client, ctx.message)}user <@someone>`", inline=False).add_field(name="Get information about your roles or someone else's", value=f"`{get_prefix(client, ctx.message)}iroles` or `{get_prefix(client, ctx.message)}roles <@someone>`", inline=False).add_field(name="Rename someone", value=f"`{get_prefix(client, ctx.message)}rename <@someone> <nickname>`", inline=False).add_field(name="Turn welcome messages on or off", value=f"`{get_prefix(client, ctx.message)}welcome <on/off>`", inline=False).add_field(name="Retrieve the last deleted message in your server", value=f"`{get_prefix(client, ctx.message)}snipe`", inline=False).add_field(name="Permanently ban someone from your server. This will override any attempts to revoke the ban via Discord's server settings.", value=f"`{get_prefix(client, ctx.message)}permaban <@someone>`", inline=False)

  embed8 = discord.Embed(title="SpaceX data commands", description="Get any information you want about space information here!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name='Closures for Boca Chica (Starbase)', value=f'`{get_prefix(client, ctx.message)}closures`', inline=False).add_field(name='Information about previous and upcoming launches', value=f'`{get_prefix(client, ctx.message)}launch <full/overview> <upcoming/previous>`', inline=False).add_field(name='Falcon booster data', value=f'`{get_prefix(client, ctx.message)}booster <booster name>`', inline=False).add_field(name='Data about SpaceX capsules', value=f'`{get_prefix(client, ctx.message)}capsules`', inline=False).add_field(name='Recovery ships used by SpaceX', value=f'`{get_prefix(client, ctx.message)}ships`', inline=False).add_field(name='Get data for a specific SpaceX rocket or a list of all rockets', value=f'`{get_prefix(client, ctx.message)}rocket` or `{get_prefix(client, ctx.message)}rocket <rocket name>`', inline=False).add_field(name='Get data about the Tesla Roadster', value=f'`{get_prefix(client, ctx.message)}roadster`', inline=False)

  embed9 = discord.Embed(title="Music commands 1", description="Vibe to your favourite tunes with Radia Music!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name= 'Join a voice channel',value = f'`{get_prefix(client, ctx.message)}join`', inline=False).add_field(name= 'Leave a voice channel',value = f'`{get_prefix(client, ctx.message)}leave`', inline=False).add_field(name= 'Play a specified song using the YouTube API. If no song is specified, I will play the server queue.',value = f'`{get_prefix(client, ctx.message)}play <song name>` or `{get_prefix(client, ctx.message)}play`', inline=False).add_field(name= 'Show the song being currently played.',value = f'`{get_prefix(client, ctx.message)}np`', inline=False).add_field(name= 'Skip to the next song in the queue',value = f'`{get_prefix(client, ctx.message)}skip`', inline=False).add_field(name= 'Get the lyrics of a song. If no song is specified, I will fetch the lyrics of the song being played.',value = f'`{get_prefix(client, ctx.message)}lyrics <song name>` or `{get_prefix(client, ctx.message)}lyrics`', inline=False).add_field(name= 'Pause the player',value = f'`{get_prefix(client, ctx.message)}pause`', inline=False).add_field(name= 'Resume the paused player',value = f'`{get_prefix(client, ctx.message)}resume`', inline=False)

  embed10 = discord.Embed(title="Music commands 2", description="Vibe to your favourite tunes with Radia Music!", color=random.choice(colors)).set_footer(icon_url=mypic, text=f'Bot created by {myname}').set_thumbnail(url=client.user.avatar_url).add_field(name= 'Show the server queue',value = f'`{get_prefix(client, ctx.message)}queue`', inline=False).add_field(name= 'Clear the server queue',value = f'`{get_prefix(client, ctx.message)}empty`', inline=False).add_field(name= 'Remove a song from the queue',value = f'`{get_prefix(client, ctx.message)}remove <index of song in queue>`', inline=False).add_field(name= 'Loop the song being played',value = f'`{get_prefix(client, ctx.message)}loop`', inline=False).add_field(name= 'Change the volume of the player',value = f'`{get_prefix(client, ctx.message)}volume <volume number>`', inline=False).add_field(name= 'View your personal playlist',value = f'`{get_prefix(client, ctx.message)}playlist view`', inline=False).add_field(name= 'Add songs to your personal playlist',value = f'`{get_prefix(client, ctx.message)}playlist add <song name>`', inline=False).add_field(name= 'Remove a song from your personal playlist',value = f'`{get_prefix(client, ctx.message)}playlist remove <index of song>`', inline=False).add_field(name= 'Add your personal playlist to the server queue',value = f'`{get_prefix(client, ctx.message)}playlist play`', inline=False)
  
  embeds = [embed1, embed2, embed3, embed4, embed5, embed7, embed8, embed9, embed10]

  await ctx.send(f'<@!{ctx.author.id}>')
  paginator = BotEmbedPaginator(ctx, embeds)
  await paginator.run()

iso = {'Abkhaz': 'ab', 'Afar': 'aa', 'Afrikaans': 'af', 'Akan': 'ak', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Aragonese': 'an', 'Armenian': 'hy', 'Assamese': 'as', 'Avaric': 'av', 'Avestan': 'ae', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bambara': 'bm', 'Bashkir': 'ba', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bihari': 'bh', 'Bislama': 'bi', 'Bosnian': 'bs', 'Breton': 'br', 'Bulgarian': 'bg', 'Burmese': 'my', 'Catalan; Valencian': 'ca', 'Chamorro': 'ch', 'Chechen': 'ce', 'Chichewa; Chewa; Nyanja': 'ny', 'Chinese': 'zh-CN', 'Taiwanese': 'zh-TW', 'Chuvash': 'cv', 'Cornish': 'kw', 'Corsican': 'co', 'Cree': 'cr', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Divehi; Dhivehi; Maldivian;': 'dv', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Ewe': 'ee', 'Faroese': 'fo', 'Fijian': 'fj', 'Finnish': 'fi', 'French': 'fr', 'Fula; Fulah; Pulaar; Pular': 'ff', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek, Modern': 'el', 'Guaraní': 'gn', 'Gujarati': 'gu', 'Haitian; Haitian Creole': 'ht', 'Hausa': 'ha', 'Hebrew (modern)': 'he', 'Herero': 'hz', 'Hindi': 'hi', 'Hiri Motu': 'ho', 'Hungarian': 'hu', 'Interlingua': 'ia', 'Indonesian': 'id', 'Interlingue': 'ie', 'Irish': 'ga', 'Igbo': 'ig', 'Inupiaq': 'ik', 'Ido': 'io', 'Icelandic': 'is', 'Italian': 'it', 'Inuktitut': 'iu', 'Japanese': 'ja', 'Javanese': 'jv', 'Kalaallisut, Greenlandic': 'kl', 'Kannada': 'kn', 'Kanuri': 'kr', 'Kashmiri': 'ks', 'Kazakh': 'kk', 'Khmer': 'km', 'Kikuyu, Gikuyu': 'ki', 'Kinyarwanda': 'rw', 'Kirghiz, Kyrgyz': 'ky', 'Komi': 'kv', 'Kongo': 'kg', 'Korean': 'ko', 'Kurdish': 'ku', 'Kwanyama, Kuanyama': 'kj', 'Latin': 'la', 'Luxembourgish, Letzeburgesch': 'lb', 'Luganda': 'lg', 'Limburgish, Limburgan, Limburger': 'li', 'Lingala': 'ln', 'Lao': 'lo', 'Lithuanian': 'lt', 'Luba-Katanga': 'lu', 'Latvian': 'lv', 'Manx': 'gv', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Māori': 'mi', 'Marathi': 'mr', 'Marshallese': 'mh', 'Mongolian': 'mn', 'Nauru': 'na', 'Navajo, Navaho': 'nv', 'Norwegian Bokmål': 'nb', 'North Ndebele': 'nd', 'Nepali': 'ne', 'Ndonga': 'ng', 'Norwegian Nynorsk': 'nn', 'Norwegian': 'no', 'Nuosu': 'ii', 'South Ndebele': 'nr', 'Occitan': 'oc', 'Ojibwe, Ojibwa': 'oj', 'Old Church Slavonic, Church Slavic, Church Slavonic, Old Bulgarian, Old Slavonic': 'cu', 'Oromo': 'om', 'Oriya': 'or', 'Ossetian, Ossetic': 'os', 'Panjabi, Punjabi': 'pa', 'Pāli': 'pi', 'Persian': 'fa', 'Polish': 'pl', 'Pashto, Pushto': 'ps', 'Portuguese': 'pt', 'Quechua': 'qu', 'Romansh': 'rm', 'Kirundi': 'rn', 'Romanian, Moldavian, Moldovan': 'ro', 'Russian': 'ru', 'Sanskrit': 'sa', 'Sardinian': 'sc', 'Sindhi': 'sd', 'Northern Sami': 'se', 'Samoan': 'sm', 'Sango': 'sg', 'Serbian': 'sr', 'Scottish Gaelic; Gaelic': 'gd', 'Shona': 'sn', 'Sinhala, Sinhalese': 'si', 'Slovak': 'sk', 'Slovene': 'sl', 'Somali': 'so', 'Southern Sotho': 'st', 'Spanish; Castilian': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swati': 'ss', 'Swedish': 'sv', 'Tamil': 'ta', 'Telugu': 'te', 'Tajik': 'tg', 'Thai': 'th', 'Tigrinya': 'ti', 'Tibetan Standard, Tibetan, Central': 'bo', 'Turkmen': 'tk', 'Tagalog': 'tl', 'Tswana': 'tn', 'Tonga': 'to', 'Turkish': 'tr', 'Tsonga': 'ts', 'Tatar': 'tt', 'Twi': 'tw', 'Tahitian': 'ty', 'Uyghur': 'ug', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz', 'Venda': 've', 'Vietnamese': 'vi', 'Volapük': 'vo', 'Walloon': 'wa', 'Welsh': 'cy', 'Wolof': 'wo', 'Western Frisian': 'fy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zhuang, Chuang': 'za'}

translator = Translator()

def ori_lang(text):
  for item in iso:
    if iso[item] == text:
      return item
    else:
      pass
      
@client.command(aliases=['translate', 'trans'])
async def Translate(ctx, arg0, *, arg1):
  try:
    t1 = arg0.lower()
    last = t1[-(len(t1)-1):]
    first = t1[:1].upper()
    final = first + last
    lang = iso[final]
  except:
    await ctx.reply(f'`{arg0}` is not in the language database.')
    return
  transltr = translator.translate(arg1, dest=lang)
  d = transltr.pronunciation
  if translator.detect(d).lang != 'en':
    em = discord.Embed(title=f'Translating to __{arg0} ({lang})__ from __{ori_lang(transltr.src).lower()} ({transltr.src})__', description = f'Translation: {transltr.text}\n\nPronunciation: {transltr.pronunciation}', color=random.choice(colors))
  else:
    em = discord.Embed(title=f'Translating to __{arg0} ({lang})__ from __{ori_lang(transltr.src).lower()} ({transltr.src})__', description = f'Translation: {transltr.text}', color=random.choice(colors))
  await ctx.reply(embed=em)

@Translate.error
async def Translate_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f'Please mention the language you want to translate to and the text you intend to translate.\nExample: {get_prefix(client, ctx.message)}translate german Hello how are you')
  elif isinstance(error, commands.CommandInvokeError):
    await ctx.reply('I could not translate the given text to the specified language.')

client.run('ODQ5ODQxMTQ2Mjg0NzM2NTEy.YLhCPg.cNEkmsxRo-1TvWVvSM2ERggmX5c')
