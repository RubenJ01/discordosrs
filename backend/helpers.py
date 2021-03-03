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
        print("sql_query")
        results = cur.fetchall()
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
