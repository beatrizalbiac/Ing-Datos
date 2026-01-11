import sqlite3
import pandas as pd
import ast

def load_bridge_pt(conn: sqlite3.Connection):
    cur = conn.cursor()
    df_pokemon = pd.read_csv("db/data/processed/pokemon_clean.csv")

    type_map = dict(conn.execute("select type_name, type_id from dim_types").fetchall()) # uses the dim_types to put the ids instead of the names 
    pokemons = dict(conn.execute("select name, pokemon_id from dim_pokemon").fetchall())

    rows = []

    for _, row in df_pokemon.iterrows(): # iterrows returns the index and the data of the row, but i dont need the index so that's why the "_"
        name = row["Name"]
        pokemon_id = pokemons.get(name)
        types = ast.literal_eval(row["Types"])

        for p, type_name in enumerate(types, start=1): # so the type_position is 1 or 2 and not 0 or 1
            type_id = type_map.get(type_name)

            rows.append((pokemon_id, type_id, p))
    
    rows_total = len(rows)

    cur.executemany(
        "insert into bridge_pokemon_types(pokemon_id, type_id, type_position) values (?, ?, ?)" \
    " on conflict(pokemon_id, type_id) do nothing", rows)

    conn.commit()
    return rows_total