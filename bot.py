import json

import requests
from discord.ext import commands

import settings.config

description = '''a dumb bot'''
bot = commands.Bot(command_prefix='!', description=description)


def armor_lookup(skill: str):
    """
    Looks up armor pieces for a skill from mhw-db.com
    :param skill: skill to lookup
    :return: list of armor names
    """
    requestUrl = "https://mhw-db.com/armor?p={\"name\": true, \"skills.skillName\": true, \"skills.level\": true}"
    apiData = requests.get(requestUrl).text
    apiObjects = json.loads(apiData)
    filteredArmor = []
    for armorPiece in apiObjects:
        for armorSkill in armorPiece['skills']:
            if armorSkill['skillName'].lower() == skill.lower():
                filteredArmor.append(armorPiece)
    output = [armorPiece['name'] for armorPiece in filteredArmor]
    return output


@bot.event
async def on_ready():
    print('hi')


@bot.command()
async def hunt(ctx, monsterName: str):
    """Looks up a monster and displays it's weaknesses."""
    await ctx.send('we\'re looking for the ' + monsterName + ' monster right now')


@bot.command()
async def armor(ctx, *, skill: str):
    """Finds all armor that has given skill"""
    await ctx.send(armor_lookup(skill))


@bot.command()
async def bees(ctx):
    """Talks about bees"""
    await ctx.send('Get on that shit yo!')


@bot.command()
async def menu(ctx):
    """Displays commands"""
    await ctx.send('!hunt')
    await ctx.send('!armor')
    await ctx.send('!bees')


bot.run(settings.config.TOKEN)
