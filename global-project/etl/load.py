import sqlite3

from load.generations import load_generations
from load.types_dim import load_types
from load.moves import load_moves
from load.abilities import load_abilities
from load.pokemons import load_pokemons


conn = sqlite3.connect("db/data/dwh.db")

try:
    load_generations(conn)
    load_types(conn)
    load_moves(conn)
    load_abilities(conn)
    load_pokemons(conn)
finally:
    conn.close()
