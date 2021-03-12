from conn import cur

"""Table for Characters with all information regarding skills as well"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS characters (
    discord_id bigint PRIMARY KEY,
    `name` varchar(20),
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

"""Bank Table"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS bank (
    discord_id bigint(20) NOT NULL,
    item_type enum ('ressource', 'equipable') NOT NULL,
    item_id int NOT NULL,
    amount int,
    PRIMARY KEY (discord_id, item_id, item_type),
    FOREIGN KEY (discord_id) REFERENCES characters(discord_id) ON DELETE CASCADE
);

"""
)

"""Agility Rooftop Lap Count"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS rooftop_courses (
    discord_id bigint NOT NULL,
    gnome_stronghold int default 0,
    draynor_village int default 0,
    al_kharid int default 0,
    varrock int default 0,
    canifis int default 0,
    falador int default 0,
    seers_village int default 0,
    pollnivneach int default 0,
    rellekka int default 0,
    ardougne int default 0,
    FOREIGN KEY (discord_id) REFERENCES characters(discord_id) ON DELETE CASCADE
)
    """
)

"""Resource Items"""
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS resource_items (
    id int auto_increment primary key,
    item_name varchar(40) NOT NULL,
    emoji_id char(18)
    )
    """
)

"""Insert items into the resource items table"""
cur.execute(
    """
    INSERT INTO resource_items (
    item_name,
    emoji_id
    )
    VALUES
    (
        'normal_log',
        '818923094923673611'
    ),
    (
        'oak_log',
        '818923095481909248'
    ),
    (
        'willow_log',
        '818923095335108678'
    ),
    (
        'teak_log',
        '818923095393566820'
    ),
    (
        'maple_log',
        '818923095192371261'
    ),
    (
        'mahogany_log',
        '818923095355686993'
    ),
    (
        'yew_log',
        '818923095376527440'
    ),
    (
        'magic_log',
        '818923095352016906'
    ),
    (
        'redwood_log',
        '818923095335108678'
    ) 
    """
)
