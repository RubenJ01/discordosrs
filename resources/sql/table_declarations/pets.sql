CREATE TABLE IF NOT EXISTS pets (
  id int auto_increment primary key,
  name varchar(40) NOT NULL,
  emoji_id int
)
/* TODO: Maybe we need columns to say which stats / skill the pet is buffing? */