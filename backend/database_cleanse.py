from conn import cur

cur.execute(
    """DROP TABLE IF EXISTS Skills"""
)
cur.execute(
    """DROP TABLE IF EXISTS Characters"""
)
cur.execute(
    """DROP TABLE IF EXISTS enemies"""
)

cur.execute(
    """DROP TABLE IF EXISTS ressource_items"""
)
cur.execute(
    """DROP TABLE IF EXISTS equipable_items"""
)
