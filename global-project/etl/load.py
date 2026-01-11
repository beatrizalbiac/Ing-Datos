import sqlite3
import datetime
import logging as log
# from pathlib import Path
import os

from load.generations import load_generations
from load.types_dim import load_types
from load.moves import load_moves
from load.abilities import load_abilities
from load.pokemons import load_pokemons
from load.bridge_pokemon_types import load_bridge_pt
from load.bridge_pokemon_abilities import load_bridge_pa
from load.fact import load_fact
from load.evolutions import update_evolutions

LOGS_DIR = "./logs/"

log.basicConfig(
    filename=f"{LOGS_DIR}load.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)


conn = sqlite3.connect("db/data/dwh.db")

start_time = datetime.datetime.now()
log.info(f"Load started at {start_time}")

total_rows = 0

try:
    total_rows += load_generations(conn)
    total_rows += load_types(conn)
    total_rows += load_moves(conn)
    total_rows += load_abilities(conn)
    total_rows += load_pokemons(conn)
    total_rows += load_bridge_pt(conn)
    total_rows += load_bridge_pa(conn)
    total_rows += load_fact(conn)

    update_evolutions(conn) # it doesn't add rows it just updates the evolutions column, so i kept it out of the log

    log.info(f"Total rows inserted into the data warehouse: {total_rows}")

except Exception:
    log.exception("Load failed with an unexpected error.")
    raise

finally:
    conn.close()
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log.info(f"Load finished at {end_time}")
    log.info(f"Total duration: {duration}")