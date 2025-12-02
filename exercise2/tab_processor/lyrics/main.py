from pathlib import Path

INPUT_DIR_VAL_OK = Path("./files/validations/ok")
OUTPUT_DIR = Path("./files/lyrics")

spanish_chords = {"do", "re", "mi", "fa", "sol", "la", "si"}

def is_chord_spanish(frag: str) -> bool:
    t = frag.strip().lower()
    if not t:
        return False

    for root in spanish_chords:
        if t.startswith(root):
            rest = t[len(root):]
            allowed_after = set("#b0123456789mM/+()")
            if all(c in allowed_after for c in rest):
                return True

    return False

def is_chord_english(frag: str) -> bool: 
    frag = frag.strip()
    if not frag:
        return False

    if frag[0] not in "ABCDEFG":
        return False

    chars = set("ABCDEFG#b0123456789mMajdimaugsl/()+o")
    if not set(frag).issubset(chars):
        return False

    if len(frag) > 6 and "/" not in frag:  # so it doesn't mistake them with lyrics
        return False

    return True
    
def is_chord(frag: str) -> bool:
    frag = frag.strip()
    if not frag:
        return False

    if is_chord_spanish(frag):
        return True

    if is_chord_english(frag):
        return True

    return False

def is_line_chord(line: str) -> bool:
    frags = line.strip().split()
    if not frags:
        return False

    chord_like = [t for t in frags if is_chord(t)]
    return len(chord_like) > 0 and len(chord_like) == len(frags)

def remove_brackets(line: str) -> str: # removes [] and the insides
    result = []
    skip = False
    for ch in line:
        if ch == "[":
            skip = True
            continue
        if ch == "]":
            skip = False
            continue
        if not skip:
            result.append(ch)
    return "".join(result)

def clean_lyrics(source: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)

    with source.open("r", encoding="latin1", errors="ignore") as f_in, \
         destination.open("w", encoding="latin1", errors="ignore") as f_out:

        for line in f_in:
            if is_line_chord(line):
                continue

            cleaned = remove_brackets(line)

            if not cleaned.strip():
                f_out.write("\n")
            else:
                f_out.write(cleaned)

def process_all():
    if not INPUT_DIR_VAL_OK.exists():
        print(f"Directory {INPUT_DIR_VAL_OK} doesn't exist.")
        return

    count = 0
    for source in INPUT_DIR_VAL_OK.rglob("*.txt"):
        rel = source.relative_to(INPUT_DIR_VAL_OK)
        destination = OUTPUT_DIR / rel.parent
        dst_path = destination / (source.stem + "_lyrics" + source.suffix)
        clean_lyrics(source, dst_path)
        count += 1

    print(f"Processed {count} files")

if __name__ == "__main__":
    process_all()