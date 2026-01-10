import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(script_path: str):
    full_path = ROOT / script_path
    print(f"\nrunning: {script_path}\n")
    subprocess.run([sys.executable, str(full_path)], check=True) # this stops if a step fails along the way


def main():
    run("db/create_db.py")

    run("etl/extract.py")

    run("etl/transform.py")

    run("etl/load.py")

    print("pipeline finished\n")


if __name__ == "__main__":
    main()