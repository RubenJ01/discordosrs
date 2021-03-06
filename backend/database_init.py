from conn import cur

"""Table for Characters with all information regarding skills as well"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS characters (
    `id` int auto_increment primary key,
    `name` varchar(20),
    `discord_id` bigint,
    `date_created` datetime DEFAULT CURRENT_TIMESTAMP,
    `last_update` datetime DEFAULT CURRENT_TIMESTAMP,
    `combat_lvl` int DEFAULT 3,
    `attack_lvl` int DEFAULT 1,
    `attack_exp` int default 0,
    `strength_lvl` int default 1,
    `strength_exp` int default 0,
    `defence_lvl` int default 1,
    `defence_exp` int default 0,
    `ranged_lvl` int default 1,
    `ranged_exp` int default 0,
    `prayer_lvl` int default 1,
    `prayer_exp` int default 0,
    `magic_lvl` int default 1,
    `magic_exp`int default 0,
    `runecraft_lvl` int default 1,
    `runecraft_exp` int default 0,
    `hitpoints_lvl` int default 1,
    `hitpoints_exp` int default 0,
    `crafting_lvl` int default 1,
    `crafting_exp` int default 0,
    `mining_lvl` int default 1,
    `mining_exp` int default 0,
    `smithing_lvl` int default 1,
    `smithing_exp` int default 0,
    `fishing_lvl` int default 1,
    `fishing_exp` int default 0,
    `cooking_lvl` int default 1,
    `cooking_exp` int default 0,
    `firemaking_lvl` int default 1,
    `firemaking_exp` int default 0,
    `woodcutting_lvl` int default 1,
    `woodcutting_exp` int default 0,
    `agility_lvl` int default 1,
    `agility_exp` int default 0,
    `herblore_lvl` int default 1,
    `herblore_exp` int default 0,
    `thieving_lvl` int default 1,
    `thieving_exp` int default 0,
    `fletching_lvl` int default 1,
    `fletching_exp` int default 0,
    `slayer_lvl` int default 1,
    `slayer_exp` int default 0,
    `farming_lvl` int default 1,
    `farming_exp` int default 0,
    `construction_lvl` int default 1,
    `construction_exp` int default 0,
    `hunter_lvl` int default 1,
    `hunter_exp` int default 0
    );
    """
)

"""
Table for NPC's
"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS non_playable_characters (
    id int auto_increment primary key,
    type enum ('boss', 'merchant', 'trainer', 'villager'),
    name varchar(40),
    combat_lvl int
    );
    """
)


"""Table for tracking boss kills

    boss_id will reference the ID of the NPC in the NPC table.
    To track the amount of times a character has killed the boss, we pull out count where uid and boss_id

    DEPENDENCIES: characters, non_playable_characters
"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS boss_kills (
    id int auto_increment primary key,
    character_id int NOT NULL,
    boss_id int,
    boss_name varchar(40),
    time_of_kill datetime DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (character_id) REFERENCES characters(id),
    FOREIGN KEY (boss_id) REFERENCES non_playable_characters(id)
    );
    """
)
