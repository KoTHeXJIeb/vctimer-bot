
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

import config

import time
import mysql.connector

bot = commands.Bot(command_prefix=config.bot_prefix)
client = discord.Client()

db = config.db_connection
cursor = db.cursor()

channels = []

@bot.event
async def on_ready():
    load()
    print('Bot is ready to go!')
    print(users, timeinvoice)
    await bot.change_presence(activity=discord.Game('meow OwO'))

@bot.command()
@commands.has_permissions(view_audit_log=True)
async def changePrefix(ctx, newPrefix):
    bot.command_prefix = newPrefix + "!"
    await ctx.send('Changes prefix to ' + newPrefix + "!")

@bot.command(help='Adds all server`s voice channels to the list (used once before start)')
async def addChannels(ctx):
    global channels, start

    start = time.time()
    channels = ctx.guild.voice_channels

    channels_names = []
    for i in channels:
        channels_names.append(i)
    end = time.time()
    res = end - start
    await ctx.send('Channels have been added. It took ' + str(round(res)) + ' seconds')
    main(channels_names)

# @bot.command(help='Checks if user is in the voice channel')
# async def checkUser(ctx, member : discord.Member):
#     voice_state = member.voice

#     if voice_state is None:
#         return await ctx.send(f'{member} is not in the voice channel!')
#     else:
#         return await ctx.send(f'{member} is in the voice channel!')

@bot.command()
async def createRole(ctx, roleName):
    guild = ctx.guild
    await guild.create_role(name=roleName)
    await ctx.send(f"Role {roleName} was created!")

def main(channel_names):

    global member_ids, end

    # for i in channel_names:
    #     if i == None:
    #         pass
    #     else:
    #         channel = client.get_channel(i)
    #         channel_names.append(channel)

    member_ids = []
    for i in channel_names:
        #members = i.members
        #members.append(i.members)
        temp = i.voice_states.keys()
        member_ids.append(temp) 

    save(member_ids)

    # for k in list(member_ids):
    #     for j in k:
    #         str(k).replace("dict_keys(", "")
    #         users.users[str(k)] = 0

    # memids = []
    # for member in members:
    #     memids.append(member.id)
    # print(memids)

def createEmbed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Embed.Empty)
    return embed

def save(ids):
    for i in ids:
        sql = 'INSERT INTO users(user_id, timeinvoice) VALUES(' + str(i) + ', "123")'
    try:
        cursor.execute(sql)
    except Exception as e:
        print('Error! Details: ' + str(e))  


def load():
    global users, timeinvoice

    users, timeinvoice = [], []
    sql = "SELECT * FROM USERS"
    
    try:
        cursor.execute(sql)

        output = cursor.fetchall()
        if len(output) <= 0:
            return
        else:
            users.append(output[1])
            timeinvoice.append(output[2])
    except Exception as e:
        print('Error! Details: ' + str(e))

bot.run(config.token)
