import discord
from discord.ext import commands
from discord.ext.commands import command
from bottoken import token, prefix


startup_extensions = [
    "cogs.wintertodt",
    "cogs.character_creation",
]

bot = commands.Bot(command_prefix=prefix, help_command=None)
bot.remove_command("help")


for extension in startup_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to load extension {extension}\n{exc}")

bot.run(token)
