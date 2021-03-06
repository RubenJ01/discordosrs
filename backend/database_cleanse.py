from conn import cur


cur.execute(
    """DROP TABLE IF EXISTS boss_kills"""
)

cur.execute(
    """DROP TABLE IF EXISTS non_playable_characters"""
)
cur.execute(
    """DROP TABLE IF EXISTS Characters"""
)

cur.execute(
    """
    DROP TABLE IF EXISTS equipable_items
    """
)
cur.execute(
    """
    DROP TABLE IF EXISTS ressource_items
    """
)
