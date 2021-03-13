CREATE TABLE IF NOT EXISTS equipable_items (
    id int auto_increment primary key,
    item_name varchar(40) NOT NULL,
    
    worn_slot enum ('head', 'cape', 'neck', 'ammunition', 'weapon', 'shield', 'two-hand', 'body', 'legs', 'hands', 'ring'),
    /* The requried lvl for equipping this item*/
    combat_lvl int DEFAULT 3,
    attack_lvl int DEFAULT 1,
    strength_lvl int default 1,
    defence_lvl int default 1,
    ranged_lvl int default 1,
    prayer_lvl int default 1,
    magic_lvl int default 1,
    runecraft_lvl int default 1,
    hitpoints_lvl int default 1,
    crafting_lvl int default 1,
    mining_lvl int default 1,
    smithing_lvl int default 1,
    fishing_lvl int default 1,
    cooking_lvl int default 1,
    firemaking_lvl int default 1,
    woodcutting_lvl int default 1,
    agility_lvl int default 1,
    herblore_lvl int default 1,
    thieving_lvl int default 1,
    fletching_lvl int default 1,
    slayer_lvl int default 1,
    farming_lvl int default 1,
    construction_lvl int default 1,
    hunter_lvl int default 1,
    /* The attack gains */
    stab_attack int default 0,
    slash_attack int default 0,
    crush_attack int default 0,
    magic_attack int default 0,
    ranged_attack int default 0,
    /* The defence gains */
    stab_defence int default 0,
    slash_defence int default 0,
    crush_defence int default 0,
    magic_defence int default 0,
    ranged_defence int default 0,
    /* Other gains*/
    strength_bonus int default 0,
    ranged_strength_bonus int default 0,
    magic_damage_bonus int default 0,
    prayer_bonus int default 0

)