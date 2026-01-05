CREATE TABLE IF NOT EXISTS dim_generations (
  generation_number INT PRIMARY KEY, -- it doubles as the id (bc it's just a number)
  region_name VARCHAR,
  release_year INT
);

CREATE TABLE IF NOT EXISTS dim_types (
  type_id SERIAL PRIMARY KEY, -- SERIAL is a prostgreSQL thing where it automaticaly increments the id (to not have to do it manually)
  type_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_abilities (
  ability_id SERIAL PRIMARY KEY,
  ability_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_pokemon (
  pokemon_id SERIAL PRIMARY KEY,
  name VARCHAR UNIQUE NOT NULL,
  tier VARCHAR,
  hp INT,
  attack INT,
  defense INT,
  special_attack INT,
  special_defense INT,
  speed INT,
  total_stats INT, -- is the metric used to differentiate legendary pokemons from normal and semi-legendary. It's js the sum of the stats
  evolves_from_id INT REFERENCES dim_pokemon(pokemon_id) -- it's a weird thing, bc if i left it as it is in the csv i'd need to create another brige table or dimension (bc one pokemon can evolve to diferent ones, such as evee, but it can only evolve from one)
);

CREATE TABLE IF NOT EXISTS dim_moves (
  move_id INT PRIMARY KEY,
  name VARCHAR UNIQUE NOT NULL,
  type_id INT REFERENCES dim_types(type_id),
  category VARCHAR,
  contest VARCHAR,
  power INT,
  accuracy INT,
  pp INT,
  generation_number INT REFERENCES dim_generations(generation_number)
);

CREATE TABLE IF NOT EXISTS fact_pokemon_moves (
  pokemon_id INT REFERENCES dim_pokemon(pokemon_id),
  move_id INT REFERENCES dim_moves(move_id),
  is_stab BOOLEAN, -- it's a pokemon mechanic where if the type of the move is the same as the type of the pokemon it has an increment on damage (I think its a 50% increment)
  PRIMARY KEY (pokemon_id, move_id)
);

CREATE TABLE IF NOT EXISTS bridge_pokemon_abilities (
  pokemon_id INT REFERENCES dim_pokemon(pokemon_id),
  ability_id INT REFERENCES dim_abilities(ability_id),
  PRIMARY KEY (pokemon_id, ability_id)
);

CREATE TABLE IF NOT EXISTS bridge_pokemon_types (
  pokemon_id INT REFERENCES dim_pokemon(pokemon_id),
  type_id INT REFERENCES dim_types(type_id),
  type_position INT NOT NULL, -- just cosmetic, because the franchise always keeps the dual types in the same order
  PRIMARY KEY (pokemon_id, type_id),
  UNIQUE (pokemon_id, type_position)
);
