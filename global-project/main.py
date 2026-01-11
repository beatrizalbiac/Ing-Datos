import datetime
import subprocess
import sys
import logging as log
from pathlib import Path
import os

LOGS_DIR = "./logs/"
ROOT = Path(__file__).resolve().parent

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("folder created")

log.basicConfig(
    filename=f"{LOGS_DIR}pipeline.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=log.INFO,
)

def run(script_path: str):
    log.info(f"Starting {script_path}")
    start_time = datetime.datetime.now()

    subprocess.run(
        [sys.executable, str(ROOT / script_path)],
        check=True
    )

    duration = datetime.datetime.now() - start_time
    log.info(f"Finished {script_path} | Duration: {duration}")

def main():
    log.info("ETL pipeline started")
    pipeline_start = datetime.datetime.now()

    run("db/create_db.py")
    run("etl/extract.py")
    run("etl/transform.py")
    run("etl/load.py")

    total_duration = datetime.datetime.now() - pipeline_start
    log.info(f"ETL pipeline finished | Total duration: {total_duration}")

if __name__ == "__main__":
    main()
