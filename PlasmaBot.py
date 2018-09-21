import discord
from discord.ext import commands

import random
import asyncio

command_prefix='p!'
bot = commands.Bot(command_prefix)

async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')

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
    game = discord.Game("killing Neonic")
    await bot.change_presence(status=discord.Status.online, activity=game)
    link1 = 'https://discord.gg/WW9Mzce'
    link2 = 'https://discord.gg/JdFBfUS'
    link3 = 'https://discord.gg/DDxdSwa'
    linkEmbed = embed = discord.Embed(title = "Plasma's Server Links", description = "Here are all of NeonicPlasma's important server links!", color=0x00ff00)
    linkEmbed.add_field(name = "Plasma's Realm (the main hub for the bot!)", value = link1)
    linkEmbed.add_field(name = "TWOW: Plasma's Race (neonic's twow)", value = link2)
    linkEmbed.add_field(name = "The Trials (neonic's camp)", value = link3)
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
    
    


bot.run("NDkyNTgyMTU4MTA0NTI2ODYx.DoYi9w.Y40pxoGfZnrJtdsfT9sCBwts0Wo")
