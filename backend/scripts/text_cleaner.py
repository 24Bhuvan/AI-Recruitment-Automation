import re
import logging
import argparse
from pathlib import Path

# -------- CONFIG --------
BASE_DIR = Path(__file__).parent.parent  # project root
DEFAULT_INPUT = BASE_DIR / "data/processed"
DEFAULT_OUTPUT = BASE_DIR / "data/processed/cleaned"

# Setup logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# -------- CLEANING FUNCTION --------
def clean_text(text: str) -> str:
    """
    Clean resume text:
    - Lowercase
    - Remove unwanted symbols (keep . , -)
    - Remove URLs, emails
    - Collapse whitespace
    """
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)

    # Remove emails
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove unwanted symbols but keep ., -
    text = re.sub(r"[^a-z0-9.,\-\s]", " ", text)

    # Collapse multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# -------- FILE PROCESSING --------
def process_file(file_path: Path, output_folder: Path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        cleaned_text = clean_text(raw_text)
        output_file = output_folder / file_path.name

        output_folder.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        logging.info(f"{file_path.name} → {output_file.name}")
    except Exception as e:
        logging.error(f"{file_path.name}: {e}")

# -------- MAIN --------
def main():
    parser = argparse.ArgumentParser(description="Clean resume text files.")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT), help="Input folder containing text files")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT), help="Output folder for cleaned files")
    args = parser.parse_args()

    input_folder = Path(args.input)
    output_folder = Path(args.output)

    if not input_folder.exists():
        logging.warning(f"Input folder not found: {input_folder}")
        return

    txt_files = [f for f in input_folder.iterdir() if f.is_file() and f.suffix == ".txt"]
    if not txt_files:
        logging.info("No .txt files found to process.")
        return

    logging.info(f"Processing {len(txt_files)} file(s)...")
    for file in txt_files:
        process_file(file, output_folder)

    logging.info("✅ Cleaning complete.")

# -------- RUN --------
if __name__ == "__main__":
    main()
