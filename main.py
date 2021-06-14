
import discord
from discord.ext import commands

import time
import MySQLdb

bot = commands.Bot(command_prefix='/')
client = discord.Client()

db = MySQLdb.connect('localhost', 'root', 'root', 'vctimer-bot')
cursor = db.cursor()

token = 'ODM4Mzg0ODAyNTgzMTUwNTk0.YI6UsQ.lnE45CDeUG6nZzwvO7hF6Q24s6k'
id = 838384802583150594

channels = []

@bot.event
async def on_ready():
    load()
    print('Bot is ready to go!')

@bot.command()
async def changePrefix(ctx, newPrefix):
    bot.command_prefix = newPrefix
    await ctx.send('Changes prefix to ' + newPrefix)

@bot.command(help='Adds all server`s voice channels to the list (used once before start)')
async def addChannels(ctx):
    global channels, start

    start = time.time()
    channels = ctx.guild.voice_channels

    channels_names = []
    for i in channels:
        await ctx.send(i)
        channels_names.append(i)
    main(channels_names)

@bot.command(help='Checks if user is in the voice channel')
async def checkUser(ctx, member : discord.Member):
    voice_state = member.voice

    if voice_state is None:
        return await ctx.send(f'{member} is not in the voice channel!')
    else:
        return await ctx.send(f'{member} is in the voice channel!')

def main(channel_names):

    global member_ids, end

    # for i in channel_names:
    #     if i == None:
    #         pass
    #     else:
    #         channel = client.get_channel(i)
    #         channel_names.append(channel)

    end = time.time()

    member_ids = []
    for i in channel_names:
        #members = i.members
        #members.append(i.members)
        temp = i.voice_states.keys()
        member_ids.append(temp)  

    for k in list(member_ids):
        for j in k:
            str(k).replace("dict_keys(", "")
            users.users[str(k)] = 0

    print(users.users)
    print(end - start)

    # memids = []
    # for member in members:
    #     memids.append(member.id)
    # print(memids)


def createEmbed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Embed.Empty)
    return embed

def save():
    for i in member_ids:
        temp = str(i)
        sql = "INSERT INTO 'users'(user_id, timeinvoice) VALUES(temp, '123')"
    cursor.execute(sql)
    db.commit()
    cursor.close()


def load():
    sql = "SELECT * FROM 'users'"
    cursor.execute(sql)
    print('Data have been loaded from DB')
    db.commit()
    cursor.close()

bot.run(token)
