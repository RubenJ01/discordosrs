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
    """
    Triggered when a user earns experience.
    - Calculates if a new level or multiple levels are gained.
    - Calculates the new experience total.
    Updates the database for the user.
    """
    skill_exp_request = f"{skill}_exp"
    skill_lvl_request = f"{skill}_lvl"
    # a list of all the skills a user can gain exp for
    valid_skills = {"firemaking_exp", "woodcutting_exp"}
    if skill_exp_request not in valid_skills:
        # the skill didnt exist so throw an error message
        embed = discord.Embed(description=f"{skill} is not a valid skill.")
        return await ctx.send(embed=embed)
    # grabbing the current level and exp amount from the user
    query = f"SELECT {skill_exp_request}, {skill_lvl_request} FROM characters WHERE discord_id = ?"
    data = await sql_query(query, (discord_id,))
    current_skill_xp = data[0][0]
    current_skill_lvl = data[0][1]
    # opening the xp_by_level.json
    path_ = Path(os.getcwd(), "resources", "xp_by_level.json")
    with open(path_, "r") as f:
        data = json.load(f)
    # calculating the new total exp amount
    new_skill_xp = current_skill_xp + amount
    if current_skill_lvl > 99:
        # player is already level 99 in that skill so just update the total exp
        query = f"UPDATE characters SET {skill_exp_request} = ? WHERE discord_id = ?"
        values = (new_skill_xp, discord_id,)
        await sql_edit(query, values)
    else:
        levels_gained = 0
        # iterating over every level in the json
        for count, xp in enumerate(data["levels"]):
            # if the level we are currently iterating over is equal to the current skill level we skip it
            if int(xp["level"]) == current_skill_lvl:
                pass
            # if the new total exp amount surpasses the one of the next level we note that the user gains
            # at least 1 level
            elif new_skill_xp >= int(xp["xp"]):
                levels_gained += 1
                # if the new total exp amount surpasses that of 99, make the level 99 and update the exp total
                if new_skill_xp >= 13034431 and int(xp["level"]) == 99:
                    new_level = data['levels'][count]['level']
                    query = f"UPDATE characters SET {skill_exp_request} = ?, " \
                            f"{skill_lvl_request} = ? WHERE discord_id = ?"
                    values = (new_skill_xp, new_level, discord_id,)
                    return await sql_edit(query, values)
            # if no levels are gained just update the total exp amount
            elif levels_gained == 0:
                query = f"UPDATE characters SET {skill_exp_request} = ? WHERE discord_id = ?"
                values = (new_skill_xp, discord_id,)
                return await sql_edit(query, values)
            # levels are gained, so the new level is update along with that total exp amount
            else:
                new_level = data['levels'][count - 1]['level']
                query = f"UPDATE characters SET {skill_exp_request} = ?, {skill_lvl_request} = ? WHERE discord_id = ?"
                values = (new_skill_xp, new_level, discord_id,)
                return await sql_edit(query, values)



