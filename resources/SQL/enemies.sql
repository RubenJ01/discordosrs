CREATE TABLE IF NOT EXISTS enemies (
    id int auto_increment primary key,
    type enum ('monster', 'boss'),
    /*race/species maybe?*/
    name varchar(40),
    
    combat_lvl int

    /*combat stats*/
    hit_points int,
    attack int,
    strength int,
    defence int,
    magic int,
    ranged int,

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
    immunte_to_poison boolean,
    immunte_to_venom boolean

    );

/*DATA*/

INSERT INTO enemies