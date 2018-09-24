import discord
from discord.ext import commands

import random
import asyncio
import os
from datetime import date

command_prefix='p!'
bot = commands.Bot(command_prefix)

@bot.event
async def on_ready():
    game = discord.Game("killing Neonic")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    welcome = bot.get_channel(492571950422556672)
    guidelines = bot.get_channel(492571898010664970)
    channel = bot.get_channel(492577748003586048)
    await channel.send("Welcome to Plasma's Realm, " + member.mention + "! We hope you have a good experience here, and make sure to read " + welcome.mention + " and " + guidelines.mention + "!")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(492577748003586048)
    await channel.send("Aww, sorry that you had to go, **" + member.name + "**#" + member.discriminator + "! I hope you come back soon!")
   
    
bot.remove_command('help')

# Minigame Related Variables:

minigameHappening = False
minigameParticipants = []
eliminationOrder = []

# Hosting Related Variables:
queue = []
currentHost = []

@bot.command()
async def ask(ctx):
    possibleresponses = [
        "Ugh... I'm too tired to answer that.",
        "Certainly... not.",
        "Go ask someone else.",
        "It's so obvious, you should already know!",
        "Absolutely, like how NeonicPlasma is dumb!",
        "Go take that to a better bot.",
        "You don't wanna know.",
        "I have literally no idea, and I hope I never do."
    ]
    number = random.randint(0, 7)
    responseChosen = possibleresponses[number]
    await ctx.send(responseChosen)

@bot.command()
async def serverlinks(ctx):
    link1 = 'https://discord.gg/WW9Mzce'
    link2 = 'https://discord.gg/JdFBfUS'
    link3 = 'https://discord.gg/DDxdSwa'
    linkEmbed = embed = discord.Embed(title = "Plasma's Server Links", description = "Here are all of NeonicPlasma's important server links!", color=0x00ff00)
    linkEmbed.add_field(name = "Plasma's Realm (the main hub for the bot!)", value = link1)
    linkEmbed.add_field(name = "TWOW: Plasma's Race (neonic's twow)", value = link2)
    linkEmbed.add_field(name = "The Trials (neonic's camp)", value = link3)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    neonicwhy = 'Use this command to see some stupid stuff Neonic has done!'
    serverlinks = "Use this command to see Neonic's important servers!"
    toggleminigames = 'Use this command to toggle your minigame status!'
    ask = "Use this command to ask me a question! Although, you might not like the answer."
    linkEmbed = embed = discord.Embed(title = "PlasmaBot Commands", description = "Need help? Here are some commands!", color=0x00ff00)
    linkEmbed.add_field(name = "p!neonicwhy", value = neonicwhy)
    linkEmbed.add_field(name = "p!serverlinks", value = serverlinks)
    linkEmbed.add_field(name = "p!toggleminigames", value = toggleminigames)
    linkEmbed.add_field(name = "p!ask", value = ask)
    await ctx.send(embed=embed)

@bot.command()
async def neonicwhy(ctx):
    possibleresponses = [
        'https://cdn.discordapp.com/attachments/492588853207629824/492603991960846347/unknown.png',
        'https://cdn.discordapp.com/attachments/492588853207629824/492603798267625483/unknown.png',
        'https://cdn.discordapp.com/attachments/492588853207629824/492604697685917706/unknown.png',
        'https://cdn.discordapp.com/attachments/492588853207629824/492604506467467264/unknown.png'
    ]
    number = random.randint(0, 3)
    responseChosen = possibleresponses[number]
    await ctx.send('neonic why ' + responseChosen)
    
@bot.command()
async def toggleminigames(ctx):
    role = discord.utils.get(ctx.message.guild.roles, name='Interested In Minigames!')
    user = ctx.message.author
    roles = user.roles
    if role in roles:
        await ctx.send('**You no longer have the Minigame role!** If you want to get it again, use p!toggleminigames.')
        await user.remove_roles(role)
    else:
        await ctx.send('**You now have the Minigame role!** If you want to remove it, use p!toggleminigames.')
        await user.add_roles(role)
        
@bot.command()
async def bombminigame(ctx, mode):
    user = ctx.message.author
    userid = user.id
    channel = ctx.message.channel
    if mode == 'queue':
        if userid in queue:
            await ctx.send(user.mention + ' has left the queue!')
            queue.remove(userid)
        else:
            await ctx.send(user.mention + ' has been added to the queue!')
            queue.append(userid)
    else:
        await ctx.send('Invalid mode!')
        
@bot.command()
async def botsend(ctx, message):
    author = ctx.message.author
    authorRoles = author.roles
    staffRole = discord.utils.get(ctx.message.guild.roles, name="Staff")
    if staffRole in authorRoles:
        channel = ctx.message.channel_mentions[0]
        await channel.send(message)
    else:
        await ctx.send('**You have no permission to use this command!**')
        
@bot.command()
async def plasmafight(ctx):
    player1hp = 150
    player2hp = 150
    embed = discord.Embed(title = '', description = 'hi hi hi hi hi')
    await ctx.send(embed = embed)
    await ctx.send(date.fromtimestamp)
        
bot.run(os.getenv('TOKEN'))
