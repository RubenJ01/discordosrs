import json
import os
from pathlib import Path

from backend.conn import cur, conn, db


async def sql_query(sql_code, values=()):
    """A function used to make database queries."""
    try:
        print(sql_code)
        print(values)
        await cur.execute(sql_code, values)
    except Exception as e:
        print(f"sql_query error: {e}")
        results = []
        return results
    else:
        results = await cur.fetchall()
        return results


async def sql_edit(sql_code, values=()):
    """A function used to make database queries."""
    try:
        cur.execute(sql_code, values)
    except Exception as e:
        print(f"sql_edit error: {e}", "dfsdfsdfdsf")
        return False
    else:
        print("Data edited")
        return True


async def gained_exp(skill, amount, discord_id):
    path_ = path_ = Path(os.getcwd(), "resources", "xp_by_level.json")
    with open(path_, "r") as f:
        data = json.load(f)
    skill = f"{skill}_exp"
    skill_exp = await sql_query("SELECT ? FROM characters WHERE discord_id = ?", (skill, discord_id,))


