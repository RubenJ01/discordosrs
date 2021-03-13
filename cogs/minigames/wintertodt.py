import random
import asyncio
import time
import math

from backend.helpers import gained_exp, check_time, sql_query
from backend.checks import has_character

import discord
from discord.ext.commands import Cog, command
from discord.ext import commands


class WinterTodt(Cog, name="Wintertodt"):
    def __init__(self, bot):
        self.bot = bot

    async def initialize_game(self, ctx):
        wintertodt_game_time = random.choice([300, 310, 320])
        points_earned = 0
        levels = await sql_query("SELECT firemaking_lvl, woodcutting_lvl FROM characters WHERE discord_id = ?",
                                 (ctx.author.id,))
        firemaking_level = levels[0][0]
        woodcutting_level = levels[0][1]
        bruma_roots = 0
        burning_bruma_roots = False
        chopping_bruma_roots = True
        firemaking_xp_earned = 0
        woodcutting_xp_earned = 0
        return [wintertodt_game_time, points_earned, firemaking_level, woodcutting_level, bruma_roots,
                burning_bruma_roots, chopping_bruma_roots, firemaking_xp_earned, woodcutting_xp_earned]

    async def start_game(self, ctx):
        values = await self.initialize_game(ctx)
        # unpacking all the values
        wintertodt_game_time = values[0]
        points_earned = values[1]
        firemaking_level = values[2]
        woodcutting_level = values[3]
        bruma_roots = values[4]
        burning_bruma_roots = values[5]
        chopping_bruma_roots = values[6]
        firemaking_xp_earned = values[7]
        woodcutting_xp_earned = values[8]
        xp_earned = 6 * firemaking_level
        activity_embed = discord.Embed(description=f"The wintertodt begins. "
                                                   f"You light the brazier earning you an additional 25 points "
                                                   f"and {xp_earned} firemaking experience "
                                                   f"{self.bot.get_emoji(815955047417380874)}.")
        activity_embed.set_image(url="https://oldschool.runescape.wiki/images/thumb/7/78/Burning_brazier_"
                                     "%28Wintertodt%29.png/687px-Burning_brazier_%28Wintertodt%29.png?7b131")
        activity_embed.set_footer(text=ctx.author.name)
        activity_embed = await ctx.send(embed=activity_embed)
        points_earned += 25
        firemaking_xp_earned += xp_earned
        game_started = True
        time_end = time.time() + (wintertodt_game_time + 1)
        await asyncio.sleep(5)
        while game_started:
            if time.time() > time_end:
                break
            else:
                danger = random.randint(1, 101)
                if danger <= 10:
                    embed = discord.Embed(
                        description="Snow falls upon you interrupting any ongoing activity.")
                    embed.set_footer(text=ctx.author.name)
                    await activity_embed.edit(embed=embed)
                elif chopping_bruma_roots:
                    xp_earned = math.ceil((woodcutting_level * 0.3) * 2)
                    bruma_roots += 2
                    embed = discord.Embed(title="Chopping Bruma Roots",
                                          description=f"You chop 2 more bruma roots "
                                                      f"{self.bot.get_emoji(815955317619163156)} "
                                                      f"and add them to your inventory "
                                                      f"({bruma_roots} total)"
                                                      f" earning you {xp_earned} woodcutting experience "
                                                      f"{self.bot.get_emoji(815955047011582053)}.")
                    embed.set_footer(text=ctx.author.name)
                    await activity_embed.edit(embed=embed)
                    woodcutting_xp_earned += xp_earned
                    if bruma_roots == 20:
                        burning_bruma_roots = True
                        chopping_bruma_roots = False
                elif burning_bruma_roots:
                    xp_earned = (firemaking_level * 3) * 2
                    points_earned += 20
                    embed = discord.Embed(title="Burning Bruma Roots",
                                          description=f"You add 2 bruma roots {self.bot.get_emoji(815955317619163156)}"
                                                      f" to the fire earning you "
                                                      f"20 points ({points_earned} total) and "
                                                      f"{xp_earned} firemaking experience "
                                                      f"{self.bot.get_emoji(815955047417380874)}.")
                    embed.set_footer(text=ctx.author.name)
                    await activity_embed.edit(embed=embed)
                    bruma_roots -= 2
                    firemaking_xp_earned += xp_earned
                    if bruma_roots == 0:
                        burning_bruma_roots = False
                        chopping_bruma_roots = True
                await asyncio.sleep(5)
        xp_earned = 100 * firemaking_level
        firemaking_xp_earned += xp_earned
        await gained_exp(ctx, "firemaking", firemaking_xp_earned)
        await gained_exp(ctx, "woodcutting", woodcutting_xp_earned)
        desc = ""
        if points_earned > 500:
            desc += f"You have reached at least 500 points earning you an additional " \
                    f"{xp_earned} firemaking experience. \n\n"
        desc += f"You earned a total of {firemaking_xp_earned} firemaking experience and " \
                f"{woodcutting_xp_earned} woodcutting experience with a total of {points_earned} points."
        embed = discord.Embed(title="The wintertodt has been subdued.",
                              description=desc)
        embed.set_image(url="https://oldschool.runescape.wiki/images/thumb/1/15/Howling_Snow_Storm.gif/300px"
                            "-Howling_Snow_Storm.gif?ec549")
        embed.set_footer(text=ctx.author.name)
        await activity_embed.edit(embed=embed)

    async def game_pause(self, ctx):
        wait_time = 60
        embed = discord.Embed(
            description=f"The next wintertodt game is about to start in {wait_time} seconds.")
        embed.set_footer(text=ctx.author.name)
        await ctx.send(embed=embed)
        embed.set_footer(text=ctx.author.name)
        await asyncio.sleep(wait_time)

    @has_character()
    @commands.group(name="wintertodt")
    async def wintertodt_game_loop(self, ctx, requested_time: int):
        values = check_time(requested_time, 1, 8)
        character_name = (await sql_query("SELECT name FROM characters WHERE discord_id = ?", (ctx.author.id,)))[0][0]
        if values[0] is True:
            embed = discord.Embed(description=f"{character_name} begins subdueing the Wintertodt for "
                                              f"{requested_time} hour(s).")
            embed.set_footer(text=ctx.author.name)
            time_started = time.time()
            time_end = time.time() + (requested_time * 3600)
            await ctx.send(embed=embed)
            while time_started < time_end:
                await self.start_game(ctx)
                if time.time() < time_end:
                    await self.game_pause(ctx)
                else:
                    break
            embed = discord.Embed(description=f"{character_name} finished doing the Wintertodt for "
                                              f"{requested_time} hour(s).")
            embed.set_footer(text=ctx.author.name)
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(embed=values[1])


def setup(bot):
    bot.add_cog(WinterTodt(bot))
