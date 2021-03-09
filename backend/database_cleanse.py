from conn import cur

cur.execute(
    """DROP TABLE IF EXISTS boss_kills"""
)

cur.execute(
    """DROP TABLE IF EXISTS bank"""
)

cur.execute(
    """DROP TABLE IF EXISTS characters"""
)

cur.execute(
    """DROP TABLE IF EXISTS equipable_items"""
)

cur.execute(
    """DROP TABLE IF EXISTS resource_items"""
)
