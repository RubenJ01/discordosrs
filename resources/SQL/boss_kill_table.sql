CREATE TABLE IF NOT EXISTS enemy_kills (
    id int auto_increment primary key,
    discord_id int NOT NULL,
    boss_id int,
    boss_name varchar(40),
    time_of_first_kill datetime DEFAULT CURRENT_TIMESTAMP,
    kill_count bigint,

    FOREIGN KEY (discord_id) REFERENCES characters(discord_id),
    /*TODO: Remove connection from enemies table so wintertodt cant join*/FOREIGN KEY (boss_id) REFERENCES enemies(id)
);