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
from backend.helpers import check_amount_in_bank, withdraw_item_from_bank, deposit_item_to_bank, sql_query, sql_edit, gained_exp, check_time
from backend.checks import has_character


class FiremakingTraining(Cog, name="Firemaking Training"):
    def __init__(self, bot):
        self.bot = bot

    @has_character()
    @commands.group(name="firemaking", invoke_without_command=True)
    async def firemaking(self, ctx):
        pass

    @has_character()
    @firemaking.command(name="stats")
    async def stats(self, ctx):
        pass

    @firemaking.command(name="light")
    async def train_firemaking(selv, ctx, log: str, requested_time: int):
        character_name = (await sql_query("SELECT name FROM characters WHERE discord_id = ?", (ctx.author.id,)))[0][0]
        path_ = Path(os.getcwd(), "resources", "fires.json")
        with open(path_, "r") as f:
            data = json.load(f)
        exists = False
        index = 0
        for count, tree in enumerate(data["fires"]):
            if log in tree["log_name"]:
                index = count
                exists = True
        if exists:
            query = "SELECT firemaking_lvl FROM characters WHERE discord_id = ?"
            values = (ctx.author.id,)
            firemaking_lvl = await sql_query(query, values)
            firemaking_lvl = firemaking_lvl[0][0]
            required_firemaking_lvl = data["fires"][index]["level_requirement"]
            log_backend_name = "normal_log" if data["fires"][
                index]["log_name"] == "normal_log" else f"{log}_log"
            # TODO: Add Emoji ID thingy
            # log_emoji = int((await sql_query("SELECT emoji_id FROM resource_items WHERE item_name = ?",
            #                                 (log_backend_name,)))[0][0])
        print(firemaking_lvl, " cur_lvl vs ",
              required_firemaking_lvl, " lvl needed to cut ", log_backend_name)
        if required_firemaking_lvl <= firemaking_lvl:
            time_check = check_time(requested_time,
                                    1, 8)
            if time_check[0] is True:
                display_log = "normal" if log == "log" else log
                embed = discord.Embed(
                    description=f"{character_name} begins lighting {display_log} logs "
                                f"for {requested_time} hour(s).")
                embed.set_footer(text=ctx.author.name)
                await ctx.send(embed=embed)
                time_started = time.time()
                time_end = time.time() + (requested_time * 60)  # TODO: This is the timer
                fires_lighted = 0
                session_fires_lighted = 0
                minutes_passed = 0
                total_minutes_passed = 0
                logs_in_inventory = 0

                session_time = 15
                xp_per_fire = data["fires"][index]["xp_per_fire"]
                xp_per_hour_at_99 = data["fires"][index]["xp_per_hour_at_99"]
                fires_per_minute = (xp_per_hour_at_99 / 60 / xp_per_fire)
                activity_embed = discord.Embed(
                    description=f"Getting ready to lighgt {display_log} logs on fire.")
                # TODO: add a picture activity_embed.set_image(url=data["trees"][index]["image"])
                activity_embed.set_footer(text=ctx.author.name)
                activity_embed = await ctx.send(embed=activity_embed)
                first_run = True
                while time_started < time_end:

                    # TODO: Add a check to see if user has enough wood for session?
                    if time.time() >= time_end:
                        firemaking_exp_gained_total = session_fires_lighted * xp_per_fire
                        # TODO: Add the embed to tell user he's finished and how much he's done.
                    logs_needed = fires_per_minute * session_time
                    await asyncio.sleep(1)  # TODO: This is the ticker time
                    # check if 1 session has has passed.
                    # TODO: Also make sure you use all the wood? (i mean it should, since it uses 1 fires_per_minute pr. minute)

                    if (minutes_passed >= session_time or (first_run == True and minutes_passed == 0)):
                        logs_in_inventory = await withdraw_item_from_bank(
                            ctx, log_backend_name, 'resource', logs_needed)
                        if not first_run:
                            xp_to_add = fires_lighted + xp_per_fire
                            await gained_exp(ctx, 'firemaking', xp_to_add)
                            fires_lighted = 0
                        first_run = False
                        minutes_passed = 0
                    total_firemaking_exp = session_fires_lighted * xp_per_fire
                    embed = discord.Embed(description=f"You light {fires_per_minute} more {display_log} fires "
                                          f"({session_fires_lighted} total) "
                                          f"for {total_firemaking_exp} firemaking experience ")
                    embed.set_footer(
                        text=f"{ctx.author.name} - Runtime: {total_minutes_passed} minute(s).")
                    await activity_embed.edit(embed=embed)
                    minutes_passed += 1
                    total_minutes_passed += 1
                    # Check if user has enough logs for the next minute.
                    if logs_in_inventory - fires_per_minute < 0:
                        activity_embed = discord.Embed(
                            description=f"You need {fires_per_minute} to continue lighting {display_log} fires, but you only have {logs_in_inventory} left.")
                        return await ctx.send(embed=activity_embed)
                    fires_lighted += fires_per_minute
                    session_fires_lighted += fires_per_minute


def setup(bot):
    bot.add_cog(FiremakingTraining(bot))
