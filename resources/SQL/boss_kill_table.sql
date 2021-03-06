    CREATE TABLE IF NOT EXISTS enemy_kills (
    id int auto_increment primary key,
    user_id int NOT NULL,
    boss_id int,
    boss_name varchar(40),
    time_of_first_kill datetime DEFAULT CURRENT_TIMESTAMP,
    kill_count bigint,

    FOREIGN KEY (user_id) REFERENCES characters(id),
    FOREIGN KEY (boss_id) REFERENCES enemies(id)
    );