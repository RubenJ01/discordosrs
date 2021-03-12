from backend.checks import has_character
from backend.helpers import sql_query

import discord
from discord.ext.commands import Cog, command
from discord.ext import commands


class AgilityTraining(Cog, name="Agility"):
    def __init__(self, bot):
        self.bot = bot

    @has_character()
    @commands.group(name="agility", invoke_without_command=True)
    async def agility(self, ctx):
        data = (await sql_query("SELECT * FROM rooftop_courses WHERE discord_id = ?", (ctx.author.id,)))[0]
        desc = f"**Gnome Stronghold Agility Course** - {data[1]} laps.\n"
        desc += f"**Draynor Village Rooftop Course** - {data[2]} laps.\n"
        desc += f"**Al Kharid Rooftop Course** - {data[3]} laps.\n"
        desc += f"**Varrock Rooftop Course** - {data[4]} laps.\n"
        desc += f"**Canifis Rooftop Course** - {data[5]} laps.\n"
        desc += f"**Falador Rooftop Course** - {data[6]} laps.\n"
        desc += f"**Seers' Village Rooftop Course** - {data[7]} laps.\n"
        desc += f"**Pollnivneach Rooftop Course** - {data[8]} laps.\n"
        desc += f"**Rellekka Rooftop Course** - {data[9]} laps.\n"
        desc += f"**Ardougne Rooftop Course** - {data[10]} laps.\n"
        embed = discord.Embed(title=f"Rooftop courses lap count {self.bot.get_emoji(819920846071005215)}",
                              description=desc)
        embed.set_footer(text=ctx.author.name)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AgilityTraining(bot))
