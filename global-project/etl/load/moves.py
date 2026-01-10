import sqlite3
import pandas as pd

def load_moves(conn: sqlite3.Connection):
    cur = conn.cursor()
    df_moves = pd.read_csv("db/data/processed/moves_clean.csv")

    types = dict(conn.execute("select type_name, type_id from dim_types").fetchall()) # uses the dim_types to put the ids instead of the names 
    df_moves["type_id"] = df_moves["Type"].map(types)

    if df_moves["type_id"].isna().any():
        missing = df_moves.loc[df_moves["type_id"].isna(), "Type"].unique().tolist()
        raise ValueError(f"Types that weren't found in dim_types: {missing}") # so it doesn't raise the error b4 executing everything, it's just for debuggin

    cols = ["Index", "Name", "type_id", "Category", "Contest", "Power", "Accuracy", "PP", "Generation"]
    rows = list(df_moves[cols].itertuples(index=False, name=None))

    cur.executemany(
        "insert into dim_moves(move_id, name, type_id, category, contest, power, accuracy, pp, generation_number) values (?, ?, ?, ?, ?, ?, ?, ?, ?)" \
    " on conflict(move_id) do nothing", rows)

    conn.commit()