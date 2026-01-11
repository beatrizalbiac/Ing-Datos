import pandas as pd
import sqlite3
import ast

def load_abilities(conn:sqlite3.Connection):
    cur = conn.cursor()
    df_pokemon = pd.read_csv("db/data/processed/pokemon_clean.csv")

    parsed = df_pokemon["Abilities"] = df_pokemon["Abilities"].apply(ast.literal_eval)

    abilities = sorted({a for list in parsed for a in list}) # so it isn't in a list per pokemon but instead "alltogether"

    rows = len(abilities)

    cur.executemany(
        "insert or ignore into dim_abilities (ability_name) values (?)",
        [(a,) for a in abilities]
    )
    conn.commit()
    return rows
