USE fpl;

CREATE TABLE if not exists players (
  player_id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  club VARCHAR(3) NOT NULL,
  position VARCHAR(50) NOT NULL,
  price DECIMAL(3, 1) NOT NULL,
  points INT UNSIGNED NOT NULL,
  value DECIMAL(5, 2),
  deviation DECIMAL(5, 2),
  deviation_by_pos DECIMAL(5, 2)
)
