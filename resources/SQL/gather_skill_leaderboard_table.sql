CREATE TABLE IF NOT EXISTS gather_skills_tracker (
    discord_id bigint(20) NOT NULL,
    item_id int(11),
    skill_name enum ('mining', 'fishing', 'woodcutting', 'farming'),
    gather_count bigint,

    PRIMARY KEY (discord_id, item_id),
    FOREIGN KEY (discord_id) REFERENCES characters(discord_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES resource_items(id) ON DELETE CASCADE
    );