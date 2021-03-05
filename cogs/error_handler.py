import math
from backend.checks import NoCharacter, HasCharacter

import discord
from discord.ext import commands



class CommandErrorHandler(commands.Cog, name='ErrorHandler'):
    """The command error handler for the bot."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Fires when a command throws an error."""
        if isinstance(error, commands.UserInputError):
            embed = discord.Embed(description="Invalid arguments! please try again.")
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            remaining_minutes, remaining_seconds = divmod(error.retry_after, 60)
            desc = f"This command is on cooldown, please retry in {int(remaining_minutes)} minutes " \
                   f"{math.ceil(remaining_seconds)} seconds."
            embed = discord.Embed(description=desc)
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(description="Too many arguments were passed! Please try again.")
            return await ctx.send(embed=embed)
        elif isinstance(error, NoCharacter):
            embed = discord.Embed(description="To use this command you need to make a character first.")
            return await ctx.send(embed=embed)
        elif isinstance(error, HasCharacter):
            embed = discord.Embed(description="You already have a character.")
            return await ctx.send(embed=embed)
        else:
            raise error


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))


