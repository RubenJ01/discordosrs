from conn import cur

cur.execute(
    """DROP TABLE IF EXISTS boss_kills"""
)

cur.execute(
    """DROP TABLE IF EXISTS bank"""
)

cur.execute(
    """DROP TABLE IF EXISTS rooftop_courses"""
)

cur.execute(
    """DROP TABLE IF EXISTS gather_skills_tracker"""
)

cur.execute(
    """DROP TABLE IF EXISTS equipable_items"""
)

cur.execute(
    """DROP TABLE IF EXISTS resource_items"""
)

# TODO: Delete at some point
cur.execute(
    """DROP TABLE IF EXISTS ressource_items"""
)
cur.execute(
    """DROP TABLE IF EXISTS pets"""
)
cur.execute(
    """DROP TABLE IF EXISTS enemy_kills"""
)

cur.execute(
    """DROP TABLE IF EXISTS enemies"""
)

cur.execute(
    """DROP TABLE IF EXISTS characters"""
)
