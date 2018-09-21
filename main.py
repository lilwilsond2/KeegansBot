from discord.ext import commands
import settings.config

bot = commands.Bot(command_prefix="!")

bot.run(settings.config.TOKEN)
