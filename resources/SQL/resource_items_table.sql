CREATE TABLE IF NOT EXISTS resource_items (
  id int auto_increment primary key,
  item_name varchar(40) NOT NULL,
  emoji_id int
)

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