import asyncio
import time
import os
import json
from random import randint
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
        self.time_started = None
        self.time_end = None
        self.amount_cut = None
        self.logs_in_inventory = None
        self.total_woodcutting_exp_gained = None
        self.activity_embed = None


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
        path_ = Path(os.getcwd(), "resources", "trees.json")
        with open(path_, "r") as f:
            data = json.load(f)
        exists = False
        index = 0
        for count, tree in enumerate(data["trees"]):
            if log in tree["log_name"]:
                index = count
                exists = True
        if exists:
            query = "SELECT woodcutting_lvl FROM characters WHERE discord_id = ?"
            values = (ctx.author.id,)
            woodcutting_lvl = await sql_query(query, values)
            woodcutting_lvl = woodcutting_lvl[0][0]
            required_woodcutting_lvl = data["trees"][index]["level_requirement"]
            self.logs_in_inventory = 0
            if required_woodcutting_lvl <= woodcutting_lvl:
                time_check = check_time(requested_time, 1, 8)
                # the function would then take "time" and return true until the time runs out
                if time_check[0] is True:
                    display_log = "normal" if log == "log" else log
                    embed = discord.Embed(
                        description=f"... begins cutting {display_log} logs for {requested_time} hour(s)")
                    await ctx.send(embed=embed)
                    self.time_started = time.time()
                    # TODO: Make sure to change this to 3600 so it's in hours :P
                    self.time_end = time.time() + (requested_time * 60)
                    logs_cut = 0
                    minutes_passed = 0
                    activity_embed = discord.Embed(description=f"Walking towards {display_log}")
                    await ctx.send(embed=activity_embed)
                    await asyncio.sleep(5)
                    while self.time_started < self.time_end:
                        effeciency_coefficient = randint(5, 10)/10
                        xp_per_log = data["trees"][index]["xp_per_log"]
                        xp_per_hour_at_99 = data["trees"][index]["xp_per_hour_at_99"]
                        logs_per_minute = round((
                            xp_per_hour_at_99 / 60 / xp_per_log) * effeciency_coefficient)
                        logs_cut = logs_cut + logs_per_minute
                        self.logs_in_inventory += logs_cut
                        woodcutting_exp_gained = logs_cut * xp_per_log
                        embed = discord.Embed(description=f"You chop {logs_per_minute} more {display_log}(s) "
                                                          f"({self.logs_in_inventory} total) for "
                                                          f"{woodcutting_exp_gained}")
                        await asyncio.sleep(60)
                        minutes_passed += 1
                        if minutes_passed >= 15:
                            self.logs_in_inventory = 0
                            minutes_passed = 0
                        if time.time() >= self.time_end:
                            break
                else:
                    return await ctx.send(embed=time_check[1])
            else:
                embed = discord.Embed(
                    description=f"You need {required_woodcutting_lvl} woodcutting to cut {log} logs.")
                return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{log} does not exist.")
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(WoodcuttingTraining(bot))
