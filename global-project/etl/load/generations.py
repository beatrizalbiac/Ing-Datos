import sqlite3

# https://docs.python.org/es/3.8/library/sqlite3.html

def load_generations(conn: sqlite3.Connection):
    cursor = conn.cursor()

    # data found on the internet
    generations = [
        (1, "Kanto", 1996),
        (2, "Johto", 1999),
        (3, "Hoenn", 2002),
        (4, "Sinnoh", 2006),
        (5, "Unova", 2010),
        (6, "Kalos", 2013),
        (7, "Alola", 2016),
        (8, "Galar", 2019),
        (9, "Paldea", 2022),
    ]
    cursor.executemany("insert into dim_generations(generation_number, region_name, release_year) values (?, ?, ?)" \
    " on conflict(generation_number) do nothing", generations)
    # I use the on conlict to nothing so it can be inserted only if it doesn't already exist, so it doesn't duplicate or overwrite things: https://hoelz.ro/blog/with-sqlite-insert-or-ignore-is-often-not-what-you-want

    conn.commit()

    # without the __init__.py it doesn't work