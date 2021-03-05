import random
import asyncio
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.helpers import gained_exp
from backend.checks import has_character

import discord
from discord.ext.commands import Cog, command


class WinterTodt(Cog, name="Wintertodt"):
    def __init__(self, bot):
        self.bot = bot
        self.wait_time = None
        self.wintertodt_game_time = None
        self.points_earned = None
        self.firemaking_level = None
        self.woodcutting_level = None
        self.bruma_roots = None
        self.burning_bruma_roots = None
        self.chopping_bruma_roots = None
        self.firemaking_xp_earned = None
        self.woodcutting_xp_earned = None
        self.activity_embed = None
        self.time_started = None
        self.time_end = None

    async def initialize_game(self):
        self.wintertodt_game_time = random.choice([300, 310, 320])
        self.points_earned = 0
        self.firemaking_level = 50
        self.woodcutting_level = 50
        self.bruma_roots = 0
        self.burning_bruma_roots = False
        self.chopping_bruma_roots = True
        self.firemaking_xp_earned = 0
        self.woodcutting_xp_earned = 0

    async def event(self, ctx):
        danger = random.randint(1, 101)
        if danger <= 10:
            embed = discord.Embed(
                description="Snow falls upon you interrupting any ongoing activity.")
            await self.activity_embed.edit(embed=embed)
        elif self.chopping_bruma_roots:
            xp_earned = int((self.woodcutting_level * 0.3) * 2)
            self.bruma_roots += 2
            embed = discord.Embed(description=f"You chop 2 more bruma roots "
                                              f"{self.bot.get_emoji(815955317619163156)} "
                                              f"and add them to your inventory "
                                              f"({self.bruma_roots} total)"
                                              f" earning you {xp_earned} woodcutting experience "
                                              f"{self.bot.get_emoji(815955047011582053)}. ")
            await self.activity_embed.edit(embed=embed)
            self.woodcutting_xp_earned += xp_earned
            if self.bruma_roots == 20:
                self.burning_bruma_roots = True
                self.chopping_bruma_roots = False
        elif self.burning_bruma_roots:
            xp_earned = (self.firemaking_level * 3) * 2
            self.points_earned += 20
            embed = discord.Embed(description=f"You add 2 bruma roots {self.bot.get_emoji(815955317619163156)}"
                                              f" to the fire earning you "
                                              f"20 points ({self.points_earned} total) and "
                                              f"{xp_earned} firemaking experience "
                                              f"{self.bot.get_emoji(815955047417380874)}.")
            await self.activity_embed.edit(embed=embed)
            self.bruma_roots -= 2
            self.firemaking_xp_earned += xp_earned
            if self.bruma_roots == 0:
                self.burning_bruma_roots = False
                self.chopping_bruma_roots = True

    async def start_game(self, ctx):
        await self.initialize_game()
        sched = AsyncIOScheduler()
        xp_earned = 6 * self.firemaking_level
        activity_embed = discord.Embed(description=f"The wintertodt begins. "
                                                   f"You light the brazier earning you an additional 25 points "
                                                   f"and {xp_earned} firemaking experience "
                                                   f"{self.bot.get_emoji(815955047417380874)}.")
        activity_embed.set_image(url="https://oldschool.runescape.wiki/images/thumb/7/78/Burning_brazier_"
                                     "%28Wintertodt%29.png/687px-Burning_brazier_%28Wintertodt%29.png?7b131")
        self.activity_embed = await ctx.send(embed=activity_embed)
        self.points_earned += 25
        self.firemaking_xp_earned += xp_earned
        sched.add_job(self.event, 'interval', args=[ctx], seconds=5)
        sched.start()
        await asyncio.sleep(self.wintertodt_game_time + 1)
        sched.shutdown()
        xp_earned = 100 * self.firemaking_level
        self.firemaking_xp_earned += xp_earned
        desc = ""
        if self.points_earned > 500:
            desc += f"You have reached at least 500 points earning you an additional " \
                    f"{xp_earned} firemaking experience. \n\n"
        desc += f"You earned a total of {self.firemaking_xp_earned} firemaking experience and " \
                f"{self.woodcutting_xp_earned} woodcutting experience with a total of {self.points_earned} points."
        embed = discord.Embed(title="The wintertodt has been subdued.",
                              description=desc)
        embed.set_image(url="https://oldschool.runescape.wiki/images/thumb/1/15/Howling_Snow_Storm.gif/300px"
                            "-Howling_Snow_Storm.gif?ec549")
        return await self.activity_embed.edit(embed=embed)

    async def game_pause(self, ctx):
        self.wait_time = 60
        embed = discord.Embed(
            description=f"The next wintertodt game is about to start in {self.wait_time} seconds.")
        await ctx.send(embed=embed)
        await asyncio.sleep(self.wait_time)

    @has_character()
    @command(name="wintertodt")
    async def wintertodt_game_loop(self, ctx, requested_time: int):
        if requested_time > 8:
            embed = discord.Embed(description="The maximum time is 8 hours.")
            return await ctx.send(embed=embed)
        elif requested_time < 1:
            embed = discord.Embed(description="The minimum time is 1 hour.")
            return await ctx.send(embed=embed)
        embed = discord.Embed(description=f"... begins subdueing the Wintertodt for {requested_time} hour(s).")
        self.time_started = time.time()
        self.time_end = time.time() + (requested_time * 3600)
        await ctx.send(embed=embed)
        while self.time_started < self.time_end:
            await self.start_game(ctx)
            if time.time() < self.time_end:
                await self.game_pause(ctx)
            else:
                break
        embed = discord.Embed(description=f"... finished doing the Wintertodt for {requested_time} hour(s).")
        return await ctx.send(embed=embed)

    @command(name="test")
    async def test(self, ctx, skill, amount: int):
        await gained_exp(ctx, skill, amount, ctx.author.id)



def setup(bot):
    bot.add_cog(WinterTodt(bot))
