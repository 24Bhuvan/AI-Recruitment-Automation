import re
from pathlib import Path

# -------- CONFIG --------
# Go up one extra level so it can access data/jd/raw outside backend/
BASE_DIR = Path(__file__).parent.parent.parent  
RAW_JD_FOLDER = BASE_DIR / "data" / "jd" / "raw"
CLEANED_JD_FOLDER = BASE_DIR / "data" / "jd" / "cleaned"
CLEANED_JD_FOLDER.mkdir(parents=True, exist_ok=True)

# -------- CLEANING FUNCTION --------
def clean_jd_text(text: str) -> str:
    """
    Clean job description text:
    - Convert to lowercase
    - Remove URLs, emails, and special characters (keep ., -)
    - Collapse multiple spaces
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-z0-9.,\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# -------- PROCESS SINGLE FILE --------
def process_jd_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_text = clean_jd_text(raw_text)
    output_file = CLEANED_JD_FOLDER / file_path.name

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"[INFO] {file_path.name} → {output_file.name}")

# -------- MAIN FUNCTION --------
def main():
    if not RAW_JD_FOLDER.exists():
        print(f"[ERROR] JD raw folder not found: {RAW_JD_FOLDER}")
        return

    jd_files = [f for f in RAW_JD_FOLDER.iterdir() if f.is_file() and f.suffix == ".txt"]

    if not jd_files:
        print(f"[WARN] No .txt files found in {RAW_JD_FOLDER}")
        return

    print(f"[INFO] Processing {len(jd_files)} job description(s)...")
    for file in jd_files:
        try:
            process_jd_file(file)
        except Exception as e:
            print(f"[ERR] Failed to clean {file.name}: {e}")

    print("[INFO] ✅ Job Description Cleaning Complete.")

# -------- RUN SCRIPT --------
if __name__ == "__main__":
    main()
