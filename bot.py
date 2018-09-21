from discord.ext import commands
import settings.config

description = '''a dumb bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('hi')

@bot.command()
async def hunt(ctx, monsterName: str):
    """Looks up a monster and displays it's weaknesses."""
    await ctx.send('we\'re looking for the ' + monsterName + ' monster right now');

@bot.command()
async def armor(ctx, skill:str):
    """Finds all armor that has given skill"""
    await ctx.send('we\'re looking for the armor with ' + skill+ ' right now')

bot.run(settings.config.TOKEN)
