CREATE TABLE IF NOT EXISTS bank (
  id int auto_increment primary key,
  user_id int,
  item_type enum ('ressource', 'equipable'),
  item_id int,
  amount int,

  FOREIGN KEY (user_id) REFERENCES characters(id)
)

/*TODO: Maybe we actually dont need an ID here, we just need to make user_id and item_id a cojoined primary key,
that way we also make sure that a user cannot add 2 lines with the same item*/