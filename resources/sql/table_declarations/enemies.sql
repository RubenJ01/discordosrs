CREATE TABLE IF NOT EXISTS enemies (
    id int auto_increment primary key,
    type enum ('monster', 'boss', 'event'),
    /*race/species maybe?*/
    name varchar(40),
    combat_lvl int default 0,
    /*combat stats*/
    hit_points int default 0,
    attack int default 0,
    strength int default 0,
    defence int default 0,
    magic int default 0,
    ranged int default 0,
    /*Agressive stats*/
    stab_attack int default 0,
    slash_attack int default 0,
    crush_attack int default 0,
    magic_attack int default 0,
    ranged_attack int default 0,
    /* The defence stats */
    stab_defence int default 0,
    slash_defence int default 0,
    crush_defence int default 0,
    magic_defence int default 0,
    ranged_defence int default 0,
    /* immunities */
    immunte_to_poison boolean default false,
    immunte_to_venom boolean default false
);