import os

FILES_DIR = "files"

SONGS_DIR = f"{FILES_DIR}/songs"
CLEANED_DIR = f"{FILES_DIR}/cleaned/songs"
VALID_OK_DIR = f"{FILES_DIR}/validations/ok/songs"
VALID_KO_DIR = f"{FILES_DIR}/validations/ko/songs"

def count(path: str) -> int:
    if not os.path.exists(path):
        return 0
    
    count = 0
    for _, _, files in os.walk(path):
        for i in files:
            if i.lower().endswith(".txt"):
                count += 1
    return count

def get_results() -> dict:
    results = {
        "songs": count(SONGS_DIR),
        "cleaned": count(CLEANED_DIR),
        "valid_ok": count(VALID_OK_DIR),
        "valid_ko": count(VALID_KO_DIR),
    }
    return results

if __name__ == "__main__":
    results = get_results()
    for name, value in results.items():
        print(f"{name}: {value} files")
