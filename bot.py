from discord.ext import commands
import settings.config
import requests
import json

description = '''a dumb bot'''
bot = commands.Bot(command_prefix='!', description=description)

def armor_lookup(skill: str):
    requestUrl = "https://mhw-db.com/armor?p={\"name\": true, \"skills.skillName\": true, \"skills.level\": true}"
    apiData = requests.get(requestUrl).text
    apiObjects = json.loads(apiData)
    outputObjects = []
    for thing in apiObjects:
        for armorSkill in thing['skills']:
            if armorSkill['skillName'] == skill:
                outputObjects.append(thing)
    output = [x['name'] for x in outputObjects]
    return output

@bot.event
async def on_ready():
    print('hi')

@bot.command()
async def hunt(ctx, monsterName: str):
    """Looks up a monster and displays it's weaknesses."""
    await ctx.send('we\'re looking for the ' + monsterName + ' monster right now')

@bot.command()
async def armor(ctx, skill: str):
    """Finds all armor that has given skill"""
    await ctx.send(armor_lookup(skill))

@bot.command()
async def bees(ctx):
    """Talks about bees"""
    await ctx.send('Get on that shit yo!')


bot.run(settings.config.TOKEN)