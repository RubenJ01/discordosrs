CREATE TABLE IF NOT EXISTS bank (
  id int auto_increment primary key,
  user_id int,
  item_type enum ('ressource', 'equipable'),
  item_id int,
  amount int,

  FOREIGN KEY (user_id) REFERENCES characters(id)
)
