import time

import discord
from discord import message
from discord.ext.commands import Cog, command
from discord.ext import commands

from backend.conn import cur, conn, db
from backend.helpers import sql_query, sql_edit, gained_exp, check_time
from backend.checks import has_character


class WoodcuttingTraining(Cog, name="Woodcutting Training"):
    def __init__(self, bot):
        self.bot = bot

    @has_character()
    @commands.group(name="woodcutting", invoke_without_command=True)
    async def woodcutting(self, ctx):
        pass

    @has_character()
    @woodcutting.command(name="stats")
    async def stats(self, ctx):
        pass

    @has_character()
    @woodcutting.command(name="cut")
    async def cut(self, ctx, log: str, requested_time: int):
        time_check = check_time(requested_time, 1, 8)
        # TODO: Maybe in the timecheck we also make the time function? like so can just do the function for as long time as the function tells us, or is that not possible?
        # the function would then take "time" and return true until the time runs out
        if time_check[0] is True:
            embed = discord.Embed(
                description=f"... begins cutting wood for {requested_time} hour(s)")

            self.time_started = time.time()
            # TODO: Make sure to change this to 3600 so it's in hours :P
            self.time_end = time.time() + (requested_time * 60)
            await ctx.send(embed=embed)
            self.amount_cut = 0

            while self.time_started < self.time_end:
                # cut some fucking wood bruh
                if time.time() >= self.time_end:
                    break
        else:
            return await ctx.send(embed=time_check[1])


def setup(bot):
    bot.add_cog(WoodcuttingTraining(bot))
