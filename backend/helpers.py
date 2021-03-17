import json
import os
import discord
import re
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
        return True


async def gained_exp(ctx, skill, amount):
    """
    Triggered when a user earns experience.
    - Calculates if a new level or multiple levels are gained.
    - Calculates the new experience total.
    Updates the database for the user.
    """
    user = ctx.author
    skill_exp_request = f"{skill}_exp"
    skill_lvl_request = f"{skill}_lvl"
    discord_id = ctx.author.id
    amount = int(amount)
    # a list of all the skills a user can gain exp for
    valid_skills = {"firemaking_exp", "woodcutting_exp"}
    if skill_exp_request not in valid_skills:
        # the skill didnt exist so throw an error message
        embed = discord.Embed(description=f"{skill} is not a valid skill.")
        return await ctx.send(embed=embed)
    # grabbing the current level and exp amount from the user
    query = f"SELECT {skill_exp_request}, {skill_lvl_request} FROM characters WHERE discord_id = ?"
    data = await sql_query(query, (discord_id,))
    current_skill_xp = int(data[0][0])
    current_skill_lvl = int(data[0][1])
    # opening the xp_by_level.json
    path_ = Path(os.getcwd(), "resources", "xp_by_level.json")
    with open(path_, "r") as f:
        data = json.load(f)
    # calculating the new total exp amount
    new_skill_xp = current_skill_xp + amount
    if current_skill_lvl >= 99:
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
                    new_level = 99
                    query = f"UPDATE characters SET {skill_exp_request} = ?, " \
                            f"{skill_lvl_request} = ? WHERE discord_id = ?"
                    values = (new_skill_xp, new_level, discord_id,)
                    # write the user a dm saying they leveled up depending on the amount of levels they gained
                    new_levels_gained = int(new_level) - int(current_skill_lvl)
                    if new_levels_gained > 1:
                        await user.send(f"Congratulations, you just advanced a {skill} level. Your {skill} level is now "
                                        f"{new_level}.")
                    elif new_levels_gained == 1:
                        await user.send(
                            f"Congratulations, you just advanced {new_levels_gained } {skill} levels. Your {skill} level "
                            f"is now {new_level}")
                    return await sql_edit(query, values)
            # if no levels are gained just update the total exp amount
            elif levels_gained == 1:
                query = f"UPDATE characters SET {skill_exp_request} = ? WHERE discord_id = ?"
                values = (new_skill_xp, discord_id,)
                return await sql_edit(query, values)
            # levels are gained, so the new level is update along with that total exp amount
            else:
                new_level = data['levels'][count - 1]['level']
                query = f"UPDATE characters SET {skill_exp_request} = ?, {skill_lvl_request} = ? WHERE discord_id = ?"
                values = (new_skill_xp, new_level, discord_id,)
                # write the user a dm saying they leveled up depending on the amount of levels they gained
                new_levels_gained = int(new_level) - int(current_skill_lvl)
                if new_levels_gained == 1:
                    await user.send(f"Congratulations, you just advanced a {skill} level. Your {skill} level is now "
                                    f"{new_level}.")
                elif new_levels_gained > 1:
                    await user.send(
                        f"Congratulations, you just advanced {new_levels_gained} {skill} levels. Your {skill} level "
                        f"is now {new_level}")
                return await sql_edit(query, values)


def check_time(requested_time):
    minimum_time = 15
    maximum_time = 8*60
    # If none of those, assume its an hour
    print(requested_time)
    minutes = re.compile('m')
    time = 0
    digits = re.compile(r'\d*')
    if not digits.search(requested_time) is None:
        time = int(digits.search(requested_time).group())
    else:
        embed = discord.Embed(
            description=f"Input {requested_time} contains no digits")
        return [0, embed]
    if minutes.search(requested_time) is None:
        time = time * 60
    if time > maximum_time:
        embed = discord.Embed(
            description=f"The maximum time is {maximum_time} hours.")
        return [0, embed]
    elif time < minimum_time:
        embed = discord.Embed(
            description=f"The minimum time is {minimum_time} hour.")
        return [0, embed]
    return [time, None]


async def deposit_item_to_bank(ctx, item, item_type, amount):
    discord_id = ctx.author.id
    item_id = 0
    # check if we got item_id or item_name in param
    if type(item) == 'int':
        item_id = item
    else:
        if item_type == 'resource':
            data = await sql_query("""
                SELECT id
                FROM resource_items
                WHERE item_name = ?
                """, (item,))
            item_id = data[0][0]
        elif item_type == 'equipable':
            data = await sql_query("""
                SELECT id
                FROM equipable_items
                WHERE item_name = ?
                """, (item,))
            item_id = data[0][0]
    # get current amount in bank for this item, type and user
    amount_in_bank = await sql_query("""
        SELECT amount
        FROM bank
        WHERE discord_id = ? and item_id = ? and item_type = ?
        """, (discord_id, item_id, item_type,))
    # if amount_in_bank.len() = 0 then insert into bank, else updtate
    if (len(amount_in_bank)) == 0:
        await sql_edit("""
        INSERT INTO bank (discord_id, item_id, item_type, amount)
        values (?, ?, ?, ?)
        """, (discord_id, item_id, item_type, amount,))
    else:
        deposit_amount = int(amount_in_bank[0][0]) + int(amount)
        await sql_edit("""
            UPDATE bank
            SET amount = ?
            WHERE discord_id = ? and item_id = ? and item_type = ?
            """, (deposit_amount, discord_id, item_id, item_type,))


async def withdraw_item_from_bank(ctx, item, item_type, amount):
    """A function to withdraw an item from the bank. It takes parameters to find what item is requested, and returns
    the amount requested, if available, else returns the amount available. example: You have 20 normal logs in the
    bank, you request to withdraw 10 to train your firemaking skill, the function returns 10. example: You have 20
    normal logs in the bank, you request to withdraw 30 to train your firemaking skill, the function returns 20.
    example: You have 0 normal logs in the bank, you request to withdraw 10 to train your firemaking skill,
    the function returns 0. """
    discord_id = ctx.author.id
    item_id = 0
    # check if we got item_id or item_name in param
    if type(item) == 'int':
        item_id = item
    else:
        if item_type == 'resource':
            data = await sql_query("""
                SELECT id
                FROM resource_items
                WHERE item_name = ?
                """, (item,))
            item_id = data[0][0]
        elif item_type == 'equipable':
            data = await sql_query("""
                SELECT id
                FROM equipable_items
                WHERE item_name = ?
                """, (item,))
            item_id = data[0][0]
    # get current amount in bank for this item, type and user
    amount_in_bank = await sql_query("""
        SELECT amount
        FROM bank
        WHERE discord_id = ? and item_id = ? and item_type = ?
        """, (discord_id, item_id, item_type,))
    # check if requested item is in the bank
    if (len(amount_in_bank)) == 0:
        return 0
    # check if requested amount is more than available amount in bank
    else:
        amount_in_bank = amount_in_bank[0][0]
        if amount_in_bank < amount:
            # delete the amount in the bank, cause all is withdrawed
            await sql_edit("""
                DELETE
                FROM bank
                WHERE discord_id = ? and item_id = ? and item_type = ?
                """, (discord_id, item_id, item_type,))
            return amount_in_bank
        else:
            amount_in_bank = amount_in_bank - amount
            await sql_edit("""
                UPDATE bank
                SET amount = ?
                WHERE discord_id = ? and item_id = ? and item_type = ?
                """, (amount_in_bank, discord_id, item_id, item_type,))
            return amount


async def check_amount_in_bank(ctx, item, item_type):
    discord_id = ctx.author.id
    item_id = 0
    # check if we got item_id or item_name in param
    if type(item) == 'int':
        item_id = item
    else:
        if item_type == 'resource':
            data = await sql_query("""
                SELECT id
                FROM resource_items
                WHERE item_name = ?
                """, (item,))
            item_id = data[0][0]
        elif item_type == 'equipable':
            data = await sql_query("""
                SELECT id
                FROM equipable_items
                WHERE item_name = ?
                """, (item,))
            item_id = data[0][0]
    # get current amount in bank for this item, type and user
    amount_in_bank = await sql_query("""
        SELECT amount
        FROM bank
        WHERE discord_id = ? and item_id = ? and item_type = ?
        """, (discord_id, item_id, item_type,))
    return amount_in_bank


async def add_kill_count(ctx, boss_id, amount_of_kills):
    """
    Adds killcount for a specific boss and user.
    If the user already has killcount for this boss update the row.
    Otherwise create a new row.
    """
    # Check if the user already has killcount for the boss
    query = f"SELECT kill_count FROM enemy_kills WHERE discord_id = ? AND boss_id = ?"
    kill_count = await sql_query(query, (ctx.author.id, boss_id,))
    if len(kill_count) == 0:
        # no killcount has been obtained yet for this boss
        # add kill count for the boss
        query = "INSERT INTO enemy_kills (discord_id, boss_id, kill_count) VALUES(?, ?, ?)"
        values = (ctx.author.id, boss_id, amount_of_kills,)
        return await sql_edit(query, values)
    else:
        # kill count has already been obtained
        # update the new kill count
        new_kill_count = kill_count[0][0] + amount_of_kills
        query = "UPDATE enemy_kills SET kill_count = ? WHERE discord_id = ? AND boss_id = ?"
        values = (new_kill_count, ctx.author.id, boss_id,)
        return await sql_edit(query, values)


# TODO: create a gathering skills tracker table, function
"""



"""
