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


@bot.event
async def on_ready():
    print(f"Logging in as {str(bot.user)}")
    print(f"{str(bot.user)} has connected to Discord!")
    print(f"Current Discord Version: {discord.__version__}")
    print(f"Number of servers currently connected to {str(bot.user)}:")
    print(len([s for s in bot.guilds]))
    print("Number of players currently connected to Bot:")
    print(sum(guild.member_count for guild in bot.guilds))


for extension in startup_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        print(f"Failed to load extension {extension}\n{exc}")

bot.run(token)
