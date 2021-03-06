import discord
from discord.ext import commands

import random
import asyncio
import os
import time

command_prefix='p!'
bot = commands.Bot(command_prefix)

game = discord.Game("fighting Neonic")

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
    guild = channel.guild
    botUser = guild.get_member(492582158104526861)
    raidProtectionRole = discord.utils.get(guild.roles, name='Raid Protection On')
    memberRole = discord.utils.get(guild.roles, name='Member')
    if raidProtectionRole in botUser.roles:
        await channel.send("Welcome to Plasma's Realm, " + member.mention + "! We hope you have a good experience here, and make sure to read " + welcome.mention + " and " + guidelines.mention + "! **Raid protection is on, so the staff will give you the member role, so please stay and be patient!**")
    else:
        await channel.send("Welcome to Plasma's Realm, " + member.mention + "! We hope you have a good experience here, and make sure to read " + welcome.mention + " and " + guidelines.mention + "!")
        await member.add_roles(memberRole)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(492577748003586048)    
    await channel.send("Aww, sorry that you had to go, **" + member.name + "**#" + member.discriminator + "! I hope you come back soon!")
   
    
bot.remove_command('help')

minigameList = {
    "1": "Pass The Bomb",
    "2": "Speed Counter"
}

# Minigame Related Variables:

minigameParticipants = []
eliminationOrder = []
minigameRunning = 0
minigamePlaying = 0
choosingMinigame = 0

currentHost = None

roundNumber = 0

# Bomb Minigame Related Variables:

holdingBomb = None
equationAnswer = 0

# Speed Counter Related Variables:

scores = {}
amountOfEmoji = 0
countingEmojiPeriod = 0

async def cancelminigame(guild):
    global holdingBomb
    global eliminationOrder
    global minigameParticipants
    global roundNumber
    global minigameRunning
    global minigamePlaying
    global currentHost
    minigameRole = discord.utils.get(guild.roles, name='Minigame Participants')
    for player in minigameRole.members:
        await player.remove_roles(minigameRole)
    minigameParticipants = []
    minigameRunning = 0
    currentHost = None

# Bomb Minigame Functions
    
async def startNewBombRound(guild):
    minigameScreenChannel = bot.get_channel(492771187332481034)
    global roundNumber
    global minigameParticipants
    global holdingBomb
    startBomb = random.choice(minigameParticipants)
    roundNumber += 1
    await minigameScreenChannel.send("**Round " + str(roundNumber) + "**\nFor this round, the bomb will start with " + startBomb.mention + ". Round starts in 5 seconds...")
    await asyncio.sleep(5)
    await minigameScreenChannel.send("**GO!**")
    holdingBomb = startBomb
    await sayBomb()
    await timer(guild)

async def sayBomb():
    global holdingBomb
    global equationAnswer
    minigameLoungeChannel = bot.get_channel(492771206500712448)
    equation1 = random.randint(1, 50)
    equation2 = random.randint(1, 50)
    equationAnswer = equation1 + equation2
    await minigameLoungeChannel.send(holdingBomb.mention + ", to pass the bomb to someone, use the `p!bpass` command followed by the answer to **" + str(equation1) + " + " + str(equation2) + "**, followed by a mention of the player you want to pass it to.")
    
async def timer(guild):
    global holdingBomb
    global eliminationOrder
    global minigameParticipants
    global roundNumber
    global minigameRunning
    global minigamePlaying
    global currentHost
    minigameRole = discord.utils.get(guild.roles, name='Minigame Participants')
    eliminatedRole = discord.utils.get(guild.roles, name='Eliminated Participants')
    await asyncio.sleep(1)
    amountOfTime = random.randint(70, 100)
    await asyncio.sleep(amountOfTime)
    personEliminated = holdingBomb
    holdingBomb = None
    minigameScreenChannel = bot.get_channel(492771187332481034)
    minigameLogChannel = bot.get_channel(494751892874854421)
    await minigameScreenChannel.send(":bomb: **The bomb exploded!** :bomb: \n" + personEliminated.mention + " had the bomb last, so they are eliminated!")
    minigameParticipants.remove(personEliminated)
    await personEliminated.remove_roles(minigameRole)
    await personEliminated.add_roles(eliminatedRole)
    eliminationOrder = [personEliminated] + eliminationOrder
    holdingBomb = None
    if len(minigameParticipants) == 1:
        winner = minigameParticipants[0]
        await minigameScreenChannel.send("**" + winner.mention + " wins __Pass The Bomb!__** Congratulations! :trophy: **Minigame ends in 10 seconds.**")
        await asyncio.sleep(10)
        for player in minigameRole.members:
            await player.remove_roles(minigameRole)
        for player in eliminatedRole.members:
            await player.remove_roles(eliminatedRole)
        logMessage = "**Congratulations to " + winner.mention + " for winning __Pass The Bomb!__\n#1: " + winner.mention + "**"
        placing = 2
        for player in eliminationOrder:
            localMessage = "\n#" + str(placing) + ": " + player.mention
            logMessage += localMessage
            placing += 1
        await minigameLogChannel.send(logMessage)
        minigameParticipants = []
        eliminationOrder = []
        roundNumber = 0
        minigameRunning = 0
        minigamePlaying = 0
        currentHost = None
    else:
        await minigameScreenChannel.send("**" + str(len(minigameParticipants)) + "** contestants remain! Next round starting in 15 seconds!")
        await asyncio.sleep(15)
        await startNewBombRound(guild)
        
# Counter Minigame Functions

async def sendNewEmojiSet(guild):
    global amountOfEmoji
    global scores
    global roundNumber
    global countingEmojiPeriod
    roundNumber += 1
    emojiSet = ["<:BookGreen:495145390560116736>", "<:BookYellow:495145295559000066>", "<:BookBlue:495145294988574720>", "<:BookRed:495145295747743754>"]
    emojiBeingUsed = random.choice(emojiSet)
    emojiString = ""
    minigameScreenChannel = bot.get_channel(492771187332481034)
    minigameLoungeChannel = bot.get_channel(492771206500712448)
    minigameRole = discord.utils.get(guild.roles, name='Minigame Participants')
    for x in range(60):
        nextEmoji = random.choice(emojiSet)
        if nextEmoji == emojiBeingUsed:
            amountOfEmoji += 1
        emojiString += nextEmoji
    await minigameScreenChannel.send("**Round " + str(roundNumber) + "**\n" + minigameRole.mention + ", the emoji you are counting this time is " + emojiBeingUsed + ". Emojis posted in 5 seconds...")
    await asyncio.sleep(5)
    countingEmojiPeriod = 1
    await minigameScreenChannel.send("**GO!**")
    await minigameScreenChannel.send(emojiString)
    await minigameScreenChannel.send("Count the amount of " + emojiBeingUsed + " and to submit it, use the `p!answer` command followed by your count. First one to get it correct gets a point!")
    
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
async def minigame(ctx, mode):
    user = ctx.message.author
    userid = user.id
    channel = ctx.message.channel
    if ctx.message.guild:
        minigameRole = discord.utils.get(ctx.message.guild.roles, name='Minigame Participants')
    global minigameRunning
    global currentHost
    global minigameParticipants
    global minigamePlaying
    global roundNumber
    global minigameList
    global choosingMinigame
    minigameScreenChannel = bot.get_channel(492771187332481034)
    minigameLogChannel = bot.get_channel(494751892874854421)
    if mode == 'create':
        if minigameRunning == 0:
            await ctx.send('**A minigame has been created!** \nPeople who would like to play can use the `p!minigame join` command to participate in the minigame!')
            minigameRunning = 1
            currentHost = user
        else:
            await ctx.send("A minigame is already happening! Please wait until the minigame has finished.")
    elif mode == 'join':
        if minigameRunning == 1:
            if minigamePlaying == 0:
                if user in minigameParticipants:
                    minigameParticipants.remove(user)
                    await ctx.send("**You have quit the minigame!** The contestant count is now **" + str(len(minigameParticipants)) + "**. If you would like to rejoin, use the `p!minigame join` command to participate again.")
                    await user.remove_roles(minigameRole)
                else:
                    minigameParticipants.append(user)
                    await user.add_roles(minigameRole)
                    if len(minigameParticipants) > 1:
                        await ctx.send("**You have joined the minigame!** The contestant count is now **" + str(len(minigameParticipants)) + "**. " + currentHost.mention + " can now use `p!minigame start` to start the minigame! If you would like to quit the minigame, use the `p!minigame join` command to quit.")
                    else:
                        await ctx.send("**You have joined the minigame!** The contestant count is now **" + str(len(minigameParticipants)) + "**. If you would like to quit the minigame, use the `p!minigame join` command to quit.") 
            else:
                await ctx.send("You cannot join or quit while a minigame is in progress!")
        else:
            await ctx.send("**A minigame is not running!** To create one, use the command `p!minigame create`.")
    elif mode == 'start':
        if user == currentHost:
            if len(minigameParticipants) > 1:
                if minigamePlaying == 0:
                    minigamePlaying = 1
                    listOfMinigameChoices = "**" + currentHost.mention + ", please choose a minigame type!** Use the `p!setminigame` command followed by the number corresponding to your minigame: "
                    for minigameNum in minigameList:
                        localString = "\n**" + minigameNum + ":** " + minigameList[minigameNum]
                        listOfMinigameChoices += localString
                    choosingMinigame = 1
                    await ctx.send(listOfMinigameChoices)
                else:
                    await ctx.send("A minigame is already being played!")
            else:
                await ctx.send("You need at least 2 people to start this minigame!")
    elif mode == 'cancel':
        if minigameRunning == 1:
            if currentHost == user:
                if isinstance(ctx.message.channel, discord.TextChannel):
                    if minigamePlaying == 0:
                        await ctx.send("Minigame has been cancelled.")
                        await cancelminigame(ctx.message.guild)
                    else:
                        await ctx.send("You cannot cancel the minigame if it has already started!")
                else:
                    await ctx.send("You cannot use this in DMs.")
            else:
                await ctx.send("You are not the host!")
        else:
            await ctx.send("There is no minigame going on right now! To start one, use `p!minigame create`.")
    else:
        await ctx.send('Invalid mode!')
        
@bot.command()
async def setminigame(ctx, number):
    global choosingMinigame
    global currentHost
    global minigameParticipants
    user = ctx.message.author
    guild = ctx.message.guild
    minigameRole = discord.utils.get(guild.roles, name='Minigame Participants')
    minigameLoungeChannel = bot.get_channel(492771206500712448)
    if choosingMinigame == 1:
        if currentHost == user:
            if number == "1":
                choosingMinigame = 0
                await ctx.send("**__Pass The Bomb__** has been initialized! Minigame starting in 10 seconds. " + minigameRole.mention + ", please head to " + minigameLoungeChannel.mention + ".")
                await asyncio.sleep(10)
                await startNewBombRound(guild)
            elif number == "2":
                choosingMinigame = 0
                global scores
                for player in minigameParticipants:
                    scores[player.id] = 0
                await ctx.send("**__Speed Counter__** has been initialized! Minigame starting in 10 seconds. " + minigameRole.mention + ", please head to " + minigameLoungeChannel.mention + ".")
                await asyncio.sleep(10)
                await sendNewEmojiSet(guild)
            elif number == "3":
                choosingMinigame = 0
                await ctx.send("**__Rise To The Limit__** has been initialized! Minigame starting in 10 seconds. " + minigameRole.mention + ", please head to " + minigameLoungeChannel.mention + ".")
                await asyncio.sleep(10)
            else:
                await ctx.send("Invalid minigame! Please try again.")
        else:
            await ctx.send("You cannot use this command!")
                
@bot.command()
async def bpass(ctx, number):
    global minigameRunning
    global minigameParticipants
    global minigamePlaying
    global holdingBomb
    global equationAnswer
    user = ctx.message.author
    if holdingBomb == user:
        personPassedTo = ctx.message.mentions[0]
        if personPassedTo:
            if personPassedTo in minigameParticipants:
                integerExists = True
                try:
                    int(number)
                except ValueError:
                    integerExists = False
                if integerExists == True:
                    if int(number) == equationAnswer:
                        holdingBomb = personPassedTo
                        await sayBomb()
                    else:
                        await ctx.send("**Wrong Answer!** Try again.")
                else:
                    await ctx.send("Make sure the number is an integer, a whole number!")
            else:
                await ctx.send("This person isn't a contestant. Pass it to someone else.")
        else:
            await ctx.send("You need to mention the person you are passing it to in your command!")
    else:
        await ctx.send("You aren't holding the bomb!")
        
@bot.command()
async def answer(ctx, number):
    minigameRole = discord.utils.get(ctx.message.guild.roles, name='Minigame Participants')
    user = ctx.message.author
    minigameScreenChannel = bot.get_channel(492771187332481034)
    minigameLogChannel = bot.get_channel(494751892874854421)
    global minigameParticipants
    global amountOfEmoji
    global countingEmojiPeriod
    global scores
    global minigameRunning
    global minigamePlaying
    global roundNumber
    global currentHost
    global eliminationOrder
    if countingEmojiPeriod == 1:
        if user in minigameParticipants:
            if int(number) == amountOfEmoji:
                couningEmojiPeriod = 0
                await ctx.send(user.mention + " is correct!")
                scores[user.id] += 1
                pointCount = scores[user.id]
                await minigameScreenChannel.send("**" + user.mention + " got it correct!** The answer was **" + str(amountOfEmoji) + "**. They now have " + str(pointCount) + " points.")  
                amountOfEmoji = 0
                if pointCount < 5:
                    await minigameScreenChannel.send("Next round in 10 seconds.")
                    await asyncio.sleep(10)
                    await sendNewEmojiSet(ctx.message.guild)
                else:
                    await minigameScreenChannel.send("**" + user.mention + " wins __Speed Counter!__** Congratulations! :trophy: **Minigame ends in 10 seconds.**")
                    await asyncio.sleep(10)
                    minigameParticipants = []
                    eliminationOrder = []
                    roundNumber = 0
                    minigameRunning = 0
                    minigamePlaying = 0
                    currentHost = None
                    for player in minigameRole.members:
                        await player.remove_roles(minigameRole)
                    logString = "**Congratulations to " + user.mention + " for winning __Speed Counter!__ \n#1: " + user.mention + " (5)**"
                    placing = 2
                    peopleWithPointCount = 0
                    for number in range(4, -1, -1):
                        if number in scores.values():
                            for key, value in scores.items():
                                if value == number:
                                    user = ctx.message.guild.get_member(int(key))
                                    localString = ""
                                    peopleWithPointCount += 1
                                    if user:
                                        localString = "\n#" + str(placing) + ": " + user.mention + " (" + str(number) + ")"
                                    else:
                                        localString = "\n#" + str(placing) + ": Cannot Find User" + " (" + str(number) + ")"
                                    logString += localString
                        placing += peopleWithPointCount
                    await minigameLogChannel.send(logString)
        else:
            await ctx.send("You are not participating in this minigame!")
                                                 
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
async def moderate(ctx, mode):
    author = ctx.message.author
    authorRoles = author.roles
    staffRole = discord.utils.get(ctx.message.guild.roles, name="Staff")
    if staffRole in authorRoles:
        guild = ctx.message.guild
        if mode == "toggleraidprotection":
            raidProtectionRole = discord.utils.get(ctx.message.guild.roles, name="Raid Protection On")
            botUser = guild.get_member(492582158104526861)
            if raidProtectionRole in botUser.roles:
                await ctx.send("Raid protection has been turned off.")
                await botUser.remove_roles(raidProtectionRole)
            else:
                await ctx.send("Raid protection has been turned on.")
                await botUser.add_roles(raidProtectionRole)
        elif mode == "warn":
            wOne = discord.utils.get(ctx.message.guild.roles, name="wOne")
            wTwo = discord.utils.get(ctx.message.guild.roles, name="wTwo")
            wThree = discord.utils.get(ctx.message.guild.roles, name="wThree")
            wFour = discord.utils.get(ctx.message.guild.roles, name="wFour")
            wFive = discord.utils.get(ctx.message.guild.roles, name="wFive")
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
