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