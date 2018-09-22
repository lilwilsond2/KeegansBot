from discord.ext import commands

from armor import getFormattedArmorOutput
from monsters import getFormattedMonsterOutput
from settings.config import TOKEN

description = '''a dumb bot'''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('hi')


@bot.command()
async def hunt(ctx, *, monsterName: str):
    """Looks up a monster and displays it's weaknesses."""
    await ctx.send(getFormattedMonsterOutput(monsterName))


@bot.command()
async def armor(ctx, *, skill: str):
    """Finds all armor that has given skill"""
    await ctx.send(getFormattedArmorOutput(skill))


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


bot.run(TOKEN)
