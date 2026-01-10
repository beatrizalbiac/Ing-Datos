CREATE TABLE IF NOT EXISTS dim_generations (
  generation_number INTEGER PRIMARY KEY, -- it doubles as the id (bc it's just a number)
  region_name TEXT,
  release_year INTEGER
);

CREATE TABLE IF NOT EXISTS dim_types (
  type_id INTEGER PRIMARY KEY AUTOINCREMENT, -- so it does the incrementation automatically. This syntax is specifically for sqlite
  type_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_abilities (
  ability_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ability_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_pokemon (
  pokemon_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  tier TEXT,
  hp INTEGER NOT NULL,
  attack INTEGER NOT NULL,
  defense INTEGER NOT NULL,
  special_attack INTEGER NOT NULL,
  special_defense INTEGER NOT NULL,
  speed INTEGER NOT NULL,
  total_stats INTEGER NOT NULL, -- is the metric used to differentiate legendary pokemons from normal and semi-legendary. It's js the sum of the stats
  evolves_from_id INTEGER REFERENCES dim_pokemon(pokemon_id) -- it's a weird thing, bc if i left it as it is in the csv i'd need to create another brige table or dimension (bc one pokemon can evolve to diferent ones, such as evee, but it can only evolve from one)
);

CREATE TABLE IF NOT EXISTS dim_moves (
  move_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  type_id INTEGER NOT NULL REFERENCES dim_types(type_id),
  category TEXT NOT NULL,
  contest TEXT,
  power INTEGER,
  accuracy INTEGER,
  pp INTEGER NOT NULL,
  generation_number INTEGER NOT NULL REFERENCES dim_generations(generation_number)
);

CREATE TABLE IF NOT EXISTS fact_pokemon_moves (
  pokemon_id INTEGER NOT NULL REFERENCES dim_pokemon(pokemon_id),
  move_id INTEGER NOT NULL REFERENCES dim_moves(move_id),
  is_stab INTEGER NOT NULL DEFAULT 0 CHECK (is_stab IN (0,1)), -- it's a pokemon mechanic where if the type of the move is the same as the type of the pokemon it has an increment on damage (I think its a 50% increment). SQLite uses 0/1 for boolean
  -- It should be a boolean but sqlite doesn't have them
  PRIMARY KEY (pokemon_id, move_id)
);

CREATE TABLE IF NOT EXISTS bridge_pokemon_abilities (
  pokemon_id INTEGER NOT NULL REFERENCES dim_pokemon(pokemon_id),
  ability_id INTEGER NOT NULL REFERENCES dim_abilities(ability_id),
  PRIMARY KEY (pokemon_id, ability_id)
);

CREATE TABLE IF NOT EXISTS bridge_pokemon_types (
  pokemon_id INTEGER NOT NULL REFERENCES dim_pokemon(pokemon_id),
  type_id INTEGER NOT NULL REFERENCES dim_types(type_id),
  type_position INTEGER NOT NULL, -- just cosmetic, because the franchise always keeps the dual types in the same order
  PRIMARY KEY (pokemon_id, type_id),
  UNIQUE (pokemon_id, type_position)
);