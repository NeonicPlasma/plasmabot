import discord
from discord.ext import commands

import random
import asyncio
import os
import time

command_prefix='p!'
bot = commands.Bot(command_prefix)

game = discord.Game("killing Neonic")

@bot.event
async def on_ready():
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

minigameParticipants = []
eliminationOrder = []
minigameRunning = 0

currentHost = ''

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
    global minigameRunning
    global currentHost
    global minigameParticipants
    if mode == 'create':
        if minigameRunning == 0:
            await ctx.send('**A game of __Pass The Bomb__ has been started!** \nPeople who would like to play can use the `p!bombminigame join` command to participate in the minigame!')
            minigameRunning = 1
            currentHost = user
        else:
            await ctx.send("A minigame is already happening! Please wait until the minigame has finished.")
    elif mode == 'join':
        if minigameRunning == 1:
            if userid in minigameParticipants:
                await ctx.send("**You have quit the minigame!** The contestant count is now **" + str(len(minigameParticipants)) + "**. If you would like to rejoin, use the `p!bombminigame join` command to participate again.")
                minigameParticipants.remove(user)
            else:
                minigameParticipants.append(user)
                if len(minigameParticipants) > 1:
                    await ctx.send("**You have joined the minigame!** The contestant count is now **" + str(len(minigameParticipants)) + "**. " + currentHost.mention + " can now use `p!bombminigame start` to start the minigame! If you would like to quit the minigame, use the `p!bombminigame join` command to quit.")
                else:
                    await ctx.send("**You have joined the minigame!** The contestant count is now **" + str(len(minigameParticipants)) + "**. If you would like to quit the minigame, use the `p!bombminigame join` command to quit.")    
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
    timeWait = 2
    player1hp = 150
    player2hp = 150
    embed = discord.Embed(title = '**Plasma Fight: Player1 vs Player 2!**', description = '', color = 0x00ff00)
    embed.add_field(name = 'Player1', value = str(player1hp) + '/150')
    embed.add_field(name = 'Player2', value = str(player2hp) + '/150')
    msg = await ctx.send("Plasma Fight!", embed = embed)
    line1 = ''
    line2 = ''
    line3 = ''
    turn = 1
    shotAt = 2
    while player1hp != 0 and player2hp != 0:
        await asyncio.sleep(timeWait)
        damageDealt = random.randint(1, 30)
        weaponUsed = ''
        action = ''
        if damageDealt >= 1 and damageDealt <= 5:
            weaponUsed = 'plasma spear'
            action = ' stabs'
        elif damageDealt >= 6 and damageDealt <= 10:
            weaponUsed = 'plasma sword'
            action = ' stabs'
        elif damageDealt >= 11 and damageDealt <= 15:
            weaponUsed = 'plasma pistol'
            action = ' shoots'
        elif damageDealt >= 16 and damageDealt <= 20:
            weaponUsed = 'plasma turret'
            action = ' shoots'
        elif damageDealt >= 21 and damageDealt <= 25:
            weaponUsed = 'plasma grenade'
            action = ' blows up'
        elif damageDealt >= 26 and damageDealt <= 30:
            weaponUsed = 'plasma reactor'
            action = ' poisons'
        line = "Player" + str(turn) + action + " Player" + str(shotAt) + " with a " + weaponUsed + " and deals " + str(damageDealt) + " damage!"
        player1hp = player1hp - 10
        line3 = line2
        line2 = line1
        line1 = line
        newembed = discord.Embed(title = '**Plasma Fight: Player1 vs Player 2!**', description = '', color = 0x00ff00)
        if line3 == '':
            if line2 == '':
                newembed.add_field(name = 'a', value = "**" + line1 + "**")
                newembed.add_field(name = 'Player1', value = str(player1hp) + '/150')
                newembed.add_field(name = 'Player2', value = str(player2hp) + '/150')
            else:
                newembed.add_field(name = 'a', value = line2)
                newembed.add_field(name = 'a', value = "**" + line1 + "**")
                newembed.add_field(name = 'Player1', value = str(player1hp) + '/150')
                newembed.add_field(name = 'Player2', value = str(player2hp) + '/150')
        else:
            newembed.add_field(name = 'a', value = line3)
            newembed.add_field(name = 'a', value = line2)
            newembed.add_field(name = 'a', value = "**" + line1 + "**")
            newembed.add_field(name = 'Player1', value = str(player1hp) + '/150')
            newembed.add_field(name = 'Player2', value = str(player2hp) + '/150')
        await ctx.send(line + "\n" + "hello") 
        await msg.edit('Plasma Fight!', embed=newembed)
        
bot.run(os.getenv('TOKEN'))
