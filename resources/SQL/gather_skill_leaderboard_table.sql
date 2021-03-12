CREATE TABLE IF NOT EXISTS gather_skills_tracker (
    id int auto_increment primary key,
    discord_id int NOT NULL,
    skill_name varchar(40),
    time_of_first_gather datetime DEFAULT CURRENT_TIMESTAMP,
    gather_count bigint,

    FOREIGN KEY (discord_id) REFERENCES characters(discord_id),
);