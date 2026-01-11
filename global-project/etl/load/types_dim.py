# I had to call it types_dim instead of just types bc that created a conflict with a python standard library also called types

import pandas as pd
import sqlite3

def load_types(conn:sqlite3.Connection):
    cur = conn.cursor()
    df_moves = pd.read_csv("db/data/processed/moves_clean.csv")

    types = sorted(df_moves["Type"].dropna().unique())

    rows = len(types)

    cur.executemany(
        "insert or ignore into dim_types (type_name) values (?)",
        [(t,) for t in types]
    )
    conn.commit()
    return rows
