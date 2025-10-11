import re
from pathlib import Path

INPUT_FOLDER = Path("data/processed")
OUTPUT_FOLDER = Path("data/processed/cleaned")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove unwanted symbols but keep ., - and ,
    text = re.sub(r"[^a-z0-9.,\-\s]", " ", text)
    
    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    cleaned_text = clean_text(raw_text)
    
    output_file = OUTPUT_FOLDER / file_path.name
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"[OK] {file_path.name} → {output_file.name}")

def main():
    files = [f for f in INPUT_FOLDER.iterdir() if f.is_file() and f.suffix == ".txt"]
    for file in files:
        try:
            process_file(file)
        except Exception as e:
            print(f"[ERR] {file.name}: {e}")

if __name__ == "__main__":
    main()
