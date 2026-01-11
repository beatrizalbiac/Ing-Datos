import sqlite3
import pandas as pd
import ast


def load_fact(conn: sqlite3.Connection):
    cur = conn.cursor()
    df = pd.read_csv("db/data/processed/pokemon_clean.csv")

    move_map = {
        name: (move_id, type_id)
        for name, move_id, type_id in cur.execute("select name, move_id, type_id from dim_moves")
    }

    pokemons = dict(cur.execute("select name, pokemon_id from dim_pokemon").fetchall())

    # stab is when any of the pokemon's types are the same as the type of the move used, that's why i need to import also the bridge pokemon type table
    ptypes = {}
    for pokemon_id, type_id in cur.execute("select pokemon_id, type_id from bridge_pokemon_types"):
        if pokemon_id not in ptypes:
            ptypes[pokemon_id] = set()
        ptypes[pokemon_id].add(type_id)

    rows = []

    for _, row in df.iterrows():
        pokemon_name = row["Name"]
        pokemon_id = pokemons.get(pokemon_name)

        moves = ast.literal_eval(row["Moves"])

        for move_name in moves:
            move_id, move_type_id = move_map[move_name]
            is_stab = 1 if move_type_id in ptypes[pokemon_id] else 0

            rows.append((pokemon_id, move_id, is_stab))

    rows_total = len(rows)

    cur.executemany(
        "insert into fact_pokemon_moves(pokemon_id, move_id, is_stab) values (?, ?, ?)" \
    " on conflict(pokemon_id, move_id) do nothing", rows)

    conn.commit()
    return rows_total