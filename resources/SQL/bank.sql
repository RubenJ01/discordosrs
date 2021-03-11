CREATE TABLE IF NOT EXISTS bank (
    discord_id bigint NOT NULL,
    item_type enum ('ressource', 'equipable') NOT NULL,
    item_id int NOT NULL,
    amount int,
    PRIMARY KEY (discord_id, item_id, item_type),
    FOREIGN KEY (discord_id) REFERENCES characters(discord_id) ON DELETE CASCADE
)
