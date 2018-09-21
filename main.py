from discord.ext import commands
import settings.config

description = '''a dumb bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('hi')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

bot.run(settings.config.TOKEN)