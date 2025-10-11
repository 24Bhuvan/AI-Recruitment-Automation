import os
from pathlib import Path
import PyPDF2
import docx2txt
from concurrent.futures import ThreadPoolExecutor, as_completed

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")
PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_path):
    return (docx2txt.process(file_path) or "").strip()

def parse_resume(file_path):
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print(f"[WARN] Unsupported file type: {file_path.name}")
        return None

def process_file(file):
    try:
        if file.is_file():
            text = parse_resume(file)
            if text:
                output_file = PROCESSED_FOLDER / f"{file.stem}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
                return f"[OK] {file.name} → {output_file.name}"
    except Exception as e:
        return f"[ERR] {file.name}: {e}"

def main():
    files = list(RAW_FOLDER.iterdir())
    with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust workers if needed
        futures = [executor.submit(process_file, f) for f in files]
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)

if __name__ == "__main__":
    main()
