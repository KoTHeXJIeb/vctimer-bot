
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

users, timeinvoice, channels = [], [], []

@bot.event
async def on_ready():
    load()
    print('Bot is ready to go!')
    await bot.change_presence(activity=discord.Game('meow OwO'))

@bot.command(help='Changes bot prefix (automatically adds "!" at the end of the prefix)')
@commands.has_permissions(view_audit_log=True)
async def changePrefix(ctx, newPrefix):
    bot.command_prefix = newPrefix + "!"
    await ctx.send('Changes prefix to ' + newPrefix + "!")

@bot.command(help='Adds all server`s voice channels to the list (used once before start)')
async def addChannels(ctx):
    global channels

    channels = ctx.guild.voice_channels
    
    channel_ids = []

    for i in channels:
        channel_ids.append(i.id)
    await ctx.send('Channels have been added.')
    print(channel_ids)
    main(channel_ids)

# @bot.command(help='Checks if user is in the voice channel')
# async def checkUser(ctx, member : discord.Member):
#     voice_state = member.voice

#     if voice_state is None:
#         return await ctx.send(f'{member} is not in the voice channel!')
#     else:
#         return await ctx.send(f'{member} is in the voice channel!')

@bot.command(help='Creates role')
async def createRole(ctx, roleName):
    guild = ctx.guild
    await guild.create_role(name=roleName)
    await ctx.send(f"Role {roleName} was created!")

def main(channel_ids):

    global member_ids

    # for i in channel_names:
    #     if i == None:
    #         pass
    #     else:
    #         channel = client.get_channel(i)
    #         channel_names.append(channel)

    member_ids = []

    for i in channel_ids:
        vc = bot.get_channel(id=i)        
        #members = i.members
        #members.append(i.members)
        temp = vc.voice_states.keys()
        if temp is None:
            break
        else:
            temp = str(temp)
            temp = temp[:len(temp) - 2]
            temp = temp[::-1]
            temp = temp[:len(temp) - 11]
            temp = temp[::-1]
            member_ids.append(temp)
    while '' in member_ids:
        member_ids.remove('')
    print(member_ids)

    n = 0

    while True:
        n += 1
        save(member_ids, n)
        time.sleep(1)

    # load()

    # save(member_ids)

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

def save(ids, n):
    for i in ids:
        sql = "INSERT INTO users (id, user_id, timeinvoice) VALUES(NULL, " + str(i) + ", " + str(n) + ")"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('Error! Details: ' + str(e))  

def load():
  
    sql = "SELECT * FROM USERS"
    
    try:
        cursor.execute(sql)

        output = cursor.fetchall()
        if len(output) <= 0:
            pass
        else:
            for i in output:
                users.append(i[1])
                timeinvoice.append(i[2])
        print(users, timeinvoice)
    except Exception as e:
        print('Error! Details: ' + str(e))

bot.run(config.token)
