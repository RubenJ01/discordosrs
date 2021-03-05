import json
import os
from pathlib import Path

from backend.conn import cur, conn, db


async def sql_query(sql_code, values=()):
    """A function used to make database queries."""
    try:
        cur.execute(sql_code, values)
    except Exception as e:
        print(f"sql_query error: {e}")
        results = []
        return results
    else:
        results = cur.fetchall()
        return results


async def sql_edit(sql_code, values=()):
    """A function used to make database queries."""
    try:
        cur.execute(sql_code, values)
    except Exception as e:
        print(f"sql_edit error: {e}")
        return False
    else:
        print("Data edited")
        return True


async def gained_exp(ctx, skill, amount, discord_id):
    skill_exp_request = f"{skill}_exp"
    skill_lvl_request = f"{skill}_lvl"
    valid_skills = {'firemaking_exp'}
    if skill_exp_request not in valid_skills:
        embed = discord.Embed(description=f"{skill} is not a valid skill.")
        return await ctx.send(embed=embed)
    query = f"SELECT {skill_exp_request}, {skill_lvl_request} FROM characters WHERE discord_id = ?"
    data = await sql_query(query, (discord_id,))
    current_skill_xp = data[0][0]
    current_skill_lvl = data[0][1]
    path_ = Path(os.getcwd(), "resources", "xp_by_level.json")
    with open(path_, "r") as f:
        data = json.load(f)
    new_skill_xp = current_skill_xp + amount
    if current_skill_lvl > 99:
        pass
    else:
        levels_gained = 0
        for count, xp in enumerate(data["levels"]):
            if int(xp["level"]) == current_skill_lvl:
                pass
            elif new_skill_xp >= int(xp["xp"]):
                levels_gained += 1
            elif levels_gained == 0:
                pass
            else:
                await ctx.send("you do not level up")
                return await ctx.send(f"you level up to level: {data['levels'][count - 1]['level']}")
