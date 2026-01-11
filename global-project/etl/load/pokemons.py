import sqlite3
import pandas as pd

def load_pokemons(conn: sqlite3.Connection):
    cur = conn.cursor()
    df_pokemon = pd.read_csv("db/data/processed/pokemon_clean.csv")

    cols = ["Name", "Tier", "HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed", "total_stats"]
    rows = list(df_pokemon[cols].itertuples(index=False, name=None))

    rows_total = len(rows)

    cur.executemany(
        "insert into dim_pokemon(name, tier, hp, attack, defense, special_attack, special_defense, speed, total_stats) values (?, ?, ?, ?, ?, ?, ?, ?, ?)" \
    " on conflict(name) do nothing", rows)

    conn.commit()
    return rows_total

    # the evolutions will be handled later as they need to be updated upon already existing data