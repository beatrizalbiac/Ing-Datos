import sqlite3
import pandas as pd
import ast


def update_evolutions(conn: sqlite3.Connection):
    cur = conn.cursor()
    df = pd.read_csv("db/data/processed/pokemon_clean.csv")

    # name -> pokemon_id
    pokemons = dict(cur.execute("select name, pokemon_id from dim_pokemon").fetchall())

    rows = []

    for _, row in df.iterrows():
        name = row["Name"]
        id = pokemons.get(name)

        evolutions = ast.literal_eval(row["Next Evolution(s)"])

        for evo_name in evolutions:
            evo_id = pokemons.get(evo_name)

            # evo evolves from base
            rows.append((id, evo_id))

    rows_total = len(rows)

    cur.executemany("update dim_pokemon set evolves_from_id = ? where pokemon_id = ?", rows)

    conn.commit()
    return rows_total
