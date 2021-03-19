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
from backend.helpers import withdraw_item_from_bank, deposit_item_to_bank, sql_query, sql_edit, gained_exp, check_time
from backend.checks import has_character


class WoodcuttingTraining(Cog, name="Woodcutting Training"):
    def __init__(self, bot):
        self.bot = bot

    @has_character()
    @commands.group(name="woodcutting", invoke_without_command=True)
    async def woodcutting(self, ctx):
        desc = f"Woodcutting is a gathering skill that primarily involves cutting down trees to obtain logs that can " \
               f"be used to make money or train other skills such as firemaking " \
               f"{self.bot.get_emoji(815955047417380874)}.\n\n" \
               f"**Usage:**\n" \
               f";woodcutting - *This message.*\n" \
               f";woodcutting stats - *Shows specifc stats about how much logs you cut.*\n" \
               f";woodcutting cut [log] [time] - *Cut a specific log for a specific amount of time*.\n" \
               f";woodcutting stop - *Stop Woodcutting.*\n" \
               f";woodcutting leaderboard - *Shows the leaderboard for the woodcutting skill.*\n\n" \
               f"**Logs:**\n" \
               f"*Normal {self.bot.get_emoji(818923094923673611)}:* level requirement = 1, xp pr. hour = 15.000.\n" \
               f"*Oak {self.bot.get_emoji(818923095481909248)}:* level requirement = 15, xp pr. hour = 40.000.\n" \
               f"*Willow {self.bot.get_emoji(818923095335108678)}:* level requirement = 30, xp pr. hour = 40.000.\n" \
               f"*Teak {self.bot.get_emoji(818923095393566820)}:* level requirement = 35, xp pr. hour = 90.000.\n" \
               f"*Maple {self.bot.get_emoji(818923095192371261)}:* level requirement = 45, xp pr. hour = 60.000.\n" \
               f"*Mahogany {self.bot.get_emoji(818923095355686993)}:* level requirement = 50, xp pr. hour = 48.000.\n" \
               f"*Yew {self.bot.get_emoji(818923095376527440)}:* level requirement = 60, xp pr. hour = 38.000.\n" \
               f"*Magic {self.bot.get_emoji(818923095352016906)}:* level requirement = 75, xp pr. hour = 30.000.\n" \
               f"*Redwood {self.bot.get_emoji(818923095335108678)}:* level requirement = 90, xp pr. hour = 70.000.\n"
        embed = discord.Embed(
            title=f"Woodcutting {self.bot.get_emoji(815955047011582053)}", description=desc)
        embed.set_footer(text=ctx.author.name)
        return await ctx.send(embed=embed)

    @has_character()
    @woodcutting.command(name="stats")
    async def stats(self, ctx):
        pass

    @has_character()
    @woodcutting.command(name="cut")
    async def cut(self, ctx, log: str, requested_time):
        character_name = (await sql_query("SELECT name FROM characters WHERE discord_id = ?", (ctx.author.id,)))[0][0]
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
            log_backend_name = "normal_log" if data["trees"][
                index]["log_name"] == "normal_log" else f"{log}_log"
            log_emoji = int((await sql_query("SELECT emoji_id FROM resource_items WHERE item_name = ?",
                                             (log_backend_name,)))[0][0])
            if required_woodcutting_lvl <= woodcutting_lvl:
                time_check = check_time(requested_time)
                if not time_check[1] == None:
                    await ctx.send(embed=time_check[1])
                # the function would then take "time" and return true until the time runs out
                if not time_check[0] == 0:
                    display_log = "normal" if log == "log" else log
                    embed = discord.Embed(
                        description=f"{character_name} begins cutting {display_log} logs {self.bot.get_emoji(log_emoji)} "
                                    f"for {requested_time} hour(s).")
                    embed.set_footer(text=ctx.author.name)
                    await ctx.send(embed=embed)
                    time_started = time.time()
                    # TODO: This is the timer
                    ticker_size = 60
                    time_end = time.time() + time_check[0] * ticker_size
                    # Predifne itteration variables
                    session_logs_cut = 0
                    minutes_passed = 0
                    total_minutes_passed = 0

                    xp_per_log = data["trees"][index]["xp_per_log"]
                    xp_per_hour_at_99 = data["trees"][index]["xp_per_hour_at_99"]
                    activity_embed = discord.Embed(
                        description=f"Walking towards {display_log} tree.")
                    activity_embed.set_image(url=data["trees"][index]["image"])
                    activity_embed.set_footer(text=ctx.author.name)
                    activity_embed = await ctx.send(embed=activity_embed)
                    while time_started < time_end:
                        time_start_current_itteration = time.time()

                        if time.time() >= time_end:
                            woodcutting_exp_gained_total = session_logs_cut * xp_per_log
                            embed = discord.Embed(title=f"{character_name} finished cutting {display_log} logs "
                                                        f"{self.bot.get_emoji(log_emoji)} "
                                                        f"for {requested_time} hour(s)",
                                                  description=f"You cut {session_logs_cut} {display_log} logs "
                                                              f"{self.bot.get_emoji(log_emoji)} earning "
                                                              f"you a total of {woodcutting_exp_gained_total} "
                                                              f"woodcutting experience "
                                                              f"{self.bot.get_emoji(815955047011582053)}.")
                            embed.set_footer(text=ctx.author.name)
                            return await ctx.send(embed=embed)
                        # Pull data + calculate stuff
                        effeciency_coefficient = randint(5, 10)/10
                        logs_per_minute = round((
                            xp_per_hour_at_99 / 60 / xp_per_log) * effeciency_coefficient)
                        # see if user looted a pet
                        # TODO: Calculate if you gained a pet exD
                        base_chance = data["trees"][index]["beaver_loot_change"]
                        # TODO: get the current woodcutting_lvl since player might've leveled up sinse last run.
                        calculate_pet_odds(
                            logs_in_inventory, base_chance, woodcutting_lvl)
                        # Iterate logs and exp
                        logs_in_inventory += logs_per_minute
                        session_logs_cut += logs_per_minute
                        woodcutting_exp_gained = logs_per_minute * xp_per_log
                        total_minutes_passed += 1
                        embed = discord.Embed(description=f"You cut {logs_per_minute} more {display_log} logs "
                                                          f"{self.bot.get_emoji(log_emoji)} ({session_logs_cut} total) "
                                                          f"for {woodcutting_exp_gained} woodcutting experience "
                                                          f"{self.bot.get_emoji(815955047011582053)}.")
                        embed.set_footer(
                            text=f"{ctx.author.name} - Runtime: {total_minutes_passed} minute(s).")
                        await activity_embed.edit(embed=embed)
                        minutes_passed += 1
                        if minutes_passed >= 15:
                            xp_to_add = logs_in_inventory * xp_per_log

                            await gained_exp(ctx, 'woodcutting', xp_to_add)
                            log_type = display_log + '_log'
                            await deposit_item_to_bank(ctx, log_type, 'resource', logs_in_inventory)
                            logs_in_inventory = 0
                            minutes_passed = 0
                        current_tick = ticker_size - \
                            (time.time() - time_start_current_itteration)
                        # ticker time
                        await asyncio.sleep(current_tick)
                else:
                    return await ctx.send(embed=time_check[1])
            else:
                embed = discord.Embed(
                    description=f"You need {required_woodcutting_lvl} woodcutting to cut {log} logs.")
                embed.set_footer(text=ctx.author.name)
                return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{log} does not exist.")
            embed.set_footer(text=ctx.author.name)
            return await ctx.send(embed=embed)

    # TODO: make a stop command for woodcutting


def calculate_pet_odds(logs_cut, base_chance, player_lvl):
    chance_to_get_beaver = (1 / (base_chance - (player_lvl * 25))) * 1000000

    for logs in range(logs_cut):
        lucky_number = randint(1, 1000000)
        print("lucky number:", lucky_number, "chance_to_get_beaver",
              chance_to_get_beaver, "base chance", base_chance)
        if chance_to_get_beaver > lucky_number:
            # TODO: We need to do a message to the player here.
            print("YOU LOOTED THE BEAVER!!!")
            pass
        else:
            # Do nothing
            print("No beaver this time buddy")
            pass
    pass
    return 0


def setup(bot):
    bot.add_cog(WoodcuttingTraining(bot))
