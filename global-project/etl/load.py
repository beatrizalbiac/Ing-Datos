import sqlite3

from load.generations import load_generations
from load.types_dim import load_types
from load.moves import load_moves
from load.abilities import load_abilities
from load.pokemons import load_pokemons
from load.bridge_pokemon_types import load_bridge_pt
from load.bridge_pokemon_abilities import load_bridge_pa
from load.fact import load_fact
from load.evolutions import update_evolutions


conn = sqlite3.connect("db/data/dwh.db")

try:
    load_generations(conn)
    load_types(conn)
    load_moves(conn)
    load_abilities(conn)
    load_pokemons(conn)
    load_bridge_pt(conn)
    load_bridge_pa(conn)
    load_fact(conn)
    update_evolutions(conn)
finally:
    conn.close()
