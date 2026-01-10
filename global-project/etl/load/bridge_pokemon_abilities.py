# basically the same as the other bridge but w/o the position
import sqlite3
import pandas as pd
import ast

def load_bridge_pa(conn: sqlite3.Connection):
    cur = conn.cursor()
    df_pokemon = pd.read_csv("db/data/processed/pokemon_clean.csv")

    ability = dict(conn.execute("select ability_name, ability_id from dim_abilities").fetchall())
    pokemons = dict(conn.execute("select name, pokemon_id from dim_pokemon").fetchall())

    rows = []

    for _, row in df_pokemon.iterrows():
        name = row["Name"]
        pokemon_id = pokemons.get(name)
        abilities = ast.literal_eval(row["Abilities"])

        for ability_name in abilities:
            ability_id = ability.get(ability_name)

            rows.append((pokemon_id, ability_id))

    cur.executemany(
        "insert into bridge_pokemon_abilities(pokemon_id, ability_id) values (?, ?)" \
    " on conflict(pokemon_id, ability_id) do nothing", rows)

    conn.commit()