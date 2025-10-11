import re
import json
from pathlib import Path
from dateparser import parse as dateparse

INPUT_FOLDER = Path("data/processed/cleaned")
OUTPUT_FOLDER = Path("data/processed/structured")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def extract_total_experience(text: str):
    patterns = [
        r"(\d+)\s*\+?\s*(?:years|yrs|year)\s*(?:of\s+)?experience",
        r"over\s+(\d+)\s*(?:years|yrs|year)",
        r"(\d+)\s*\+?\s*(?:years|yrs|year)"
    ]
    matches = []
    for pat in patterns:
        for match in re.findall(pat, text.lower()):
            try:
                matches.append(int(match))
            except:
                continue
    return max(matches) if matches else None

def clean_parentheses(s: str):
    while s.count("(") > s.count(")"):
        s = s.replace("(", "", 1)
    while s.count(")") > s.count("("):
        s = s.replace(")", "", 1)
    return s

def extract_roles_and_durations(text: str):
    text = text.replace("–", "-").replace("—", "-").replace("to", "-")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    roles = []

    # SAFER regex: title is anything before a date or duration, no literal parentheses required
    role_pattern = re.compile(
        r"(?P<title>.+?)\s*[,–-]?\s*(?P<duration>(?:\w+\s*\d{4}|\d{4})\s*-\s*(?:present|\w+\s*\d{4}|\d{4})|\d+\s*(?:years|yrs))",
        re.IGNORECASE
    )

    for line in lines:
        line = clean_parentheses(line)
        for m in role_pattern.finditer(line):
            title = m.group("title").strip()
            dur = m.group("duration").strip().lower()

            start_year = end_year = None
            if "-" in dur:
                parts = [p.strip() for p in dur.split("-")]
                try:
                    start_year = dateparse(parts[0]).year
                except:
                    start_year = None
                if "present" in parts[1]:
                    end_year = None
                else:
                    try:
                        end_year = dateparse(parts[1]).year
                    except:
                        end_year = None
            else:
                num = re.search(r"\d+", dur)
                if num:
                    start_year = None
                    end_year = int(num.group(0))

            roles.append({
                "title": title,
                "duration_raw": dur,
                "start_year": start_year,
                "end_year": end_year
            })

    return roles

def process_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        total_exp = extract_total_experience(text)
        roles = extract_roles_and_durations(text)

        result = {
            "name": file_path.stem,
            "total_experience_years": total_exp,
            "roles": roles
        }

        output_file = OUTPUT_FOLDER / f"{file_path.stem}_experience.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"[OK] {file_path.name} → {output_file.name} ({len(roles)} roles found, total={total_exp})")

    except Exception as e:
        print(f"[ERR] {file_path.name}: {e}")

def main():
    files = [f for f in INPUT_FOLDER.iterdir() if f.is_file() and f.suffix == ".txt"]
    for file in files:
        process_file(file)

if __name__ == "__main__":
    main()
