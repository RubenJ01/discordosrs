from conn import cur

cur.execute(
    """DROP TABLE IF EXISTS Skills"""

)
cur.execute(
    """DROP TABLE IF EXISTS Characters"""
)
