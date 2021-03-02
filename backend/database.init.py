from conn import conn

cur = conn.cursor()


# Create Characters Table

cur.execute(
    """CREATE TABLE IF NOT EXISTS Characters (
    `id` int auto_increment primary key,
    `name` varchar(20),
    `discord_id` bigint,
    `date_created` datetime DEFAULT CURRENT_TIMESTAMP,
    `last_update` datetime DEFAULT CURRENT_TIMESTAMP,
    `combat_lvl` int DEFAULT 3

  );""")


# Create Skills & Stats table
cur.execute(
    """ 
    CREATE TABLE IF NOT EXISTS Skills (
      `id` int auto_increment primary key, 
      `user_id` int NOT NULL,
      `attack_lvl` int default 1,
      ´attack_exp´ int default 0,

      FOREIGN KEY (user_id) REFERENCES Characters(id)
    );"""
)
