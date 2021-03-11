import asyncio
import time
import os
import json
from random import randint
from pathlib import Path

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
            logs_in_inventory = 0
            if required_woodcutting_lvl <= woodcutting_lvl:
                time_check = check_time(requested_time, 1, 8)
                # the function would then take "time" and return true until the time runs out
                if time_check[0] is True:
                    display_log = "normal" if log == "log" else log
                    embed = discord.Embed(
                        description=f"... begins cutting {display_log} logs for {requested_time} hour(s)")
                    await ctx.send(embed=embed)
                    time_started = time.time()
                    # TODO: Make sure to change this to 3600 so it's in hours :P
                    time_end = time.time() + (requested_time * 60)
                    # Predifne itteration variables
                    session_logs_cut = 0
                    minutes_passed = 0
                    activity_embed = discord.Embed(
                        description=f"Walking towards {display_log}")
                    activity_embed = await ctx.send(embed=activity_embed)
                    while time_started < time_end:
                        if time.time() >= time_end:
                            embed = discord.Embed(description="Done")
                            return await ctx.send(embed=embed)
                        await asyncio.sleep(1)
                        # Pull data + calculate stuff
                        effeciency_coefficient = randint(5, 10)/10
                        xp_per_log = data["trees"][index]["xp_per_log"]
                        xp_per_hour_at_99 = data["trees"][index]["xp_per_hour_at_99"]
                        logs_per_minute = round((
                            xp_per_hour_at_99 / 60 / xp_per_log) * effeciency_coefficient)
                        # Iterate logs and exp
                        logs_in_inventory = logs_in_inventory + logs_per_minute
                        session_logs_cut = session_logs_cut + logs_per_minute
                        woodcutting_exp_gained_total = session_logs_cut * xp_per_log
                        woodcutting_exp_gained = logs_per_minute * xp_per_log
                        embed = discord.Embed(description=f"You chop {logs_per_minute} more {display_log}(s) "
                                                          f"({logs_in_inventory} total) for "
                                                          f"{woodcutting_exp_gained}")
                        await activity_embed.edit(embed=embed)
                        minutes_passed += 1
                        print(minutes_passed)
                        if minutes_passed >= 15:
                            # TODO: Send exp earned to the DB.
                            # TODO: Do we need to call the gained_exp command as well?
                            xp_to_add = logs_in_inventory * xp_per_log
                            await gained_exp(ctx, 'woodcutting', xp_to_add)
                            # TODO: Send logs in inventory into the bank

                            logs_in_inventory = 0
                            minutes_passed = 0

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
