import re
import json
from pathlib import Path

# ===== Paths =====
INPUT_FOLDER = Path("data/processed/cleaned")
OUTPUT_FOLDER = Path("data/processed/structured")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ===== Degree & institution detection =====
DEGREES = [
    "b\\.tech", "btech", "bachelor", "b\\.e", "be",
    "m\\.tech", "mtech", "master", "m\\.s", "ms",
    "mba", "ph\\.d", "phd", "bsc", "msc", "bca", "mca",
    "ba", "ma", "bcom", "mcom", "diploma", "associate"
]

def extract_education_entries(text: str):
    """
    Detect degree, institution, and year patterns.
    Returns list of dicts with degree, institute, and year.
    """
    entries = []
    text_lower = text.lower()

    degree_pattern = r"(" + "|".join(DEGREES) + r")"
    year_pattern = r"(19|20)\d{2}"
    inst_pattern = r"(university|college|institute|school|academy|iit|nit|iiit|univ|polytechnic)"

    lines = text.splitlines()
    for line in lines:
        l = line.strip().lower()
        if not l:
            continue

        degree_match = re.search(degree_pattern, l)
        inst_match = re.search(inst_pattern, l)
        year_match = re.search(year_pattern, l)

        if degree_match:
            entries.append({
                "degree": degree_match.group(1),
                "institute": inst_match.group(1) if inst_match else None,
                "year": year_match.group(0) if year_match else None,
                "raw_text": line.strip()
            })

    return entries

# ===== Main processor =====
def process_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        education_entries = extract_education_entries(text)

        result = {
            "name": file_path.stem,
            "education": education_entries
        }

        output_file = OUTPUT_FOLDER / f"{file_path.stem}_education.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"[OK] {file_path.name} → {output_file.name} ({len(education_entries)} entries)")

    except Exception as e:
        print(f"[ERR] {file_path.name}: {e}")

# ===== Runner =====
def main():
    files = [f for f in INPUT_FOLDER.iterdir() if f.is_file() and f.suffix == ".txt"]
    for file in files:
        process_file(file)

if __name__ == "__main__":
    main()
