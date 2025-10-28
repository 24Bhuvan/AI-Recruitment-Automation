import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# --- PATHS ---
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FOLDER = BASE_DIR / "data/processed/cleaned"
OUTPUT_FOLDER = BASE_DIR / "data/processed/structured"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# --- MODEL LOADING ---
print("[INFO] Loading model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("[INFO] Model loaded successfully.")

# --- STRUCTURING FUNCTION ---
def structure_resume(text):
    sections = {
        "education": [],
        "experience": [],
        "skills": []
    }
    for line in text.split("\n"):
        l = line.lower()
        if "b.tech" in l or "bachelor" in l or "degree" in l:
            sections["education"].append(line.strip())
        elif "intern" in l or "engineer" in l or "developer" in l or "experience" in l:
            sections["experience"].append(line.strip())
        elif any(skill in l for skill in ["python", "java", "sql", "ml", "ai", "excel", "communication"]):
            sections["skills"].append(line.strip())
    return sections

# --- PROCESSING FUNCTION ---
def process_resume(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    structured = structure_resume(text)
    embedding = model.encode(text)

    out_base = OUTPUT_FOLDER / file_path.stem
    for sec, content in structured.items():
        json_path = OUTPUT_FOLDER / f"{file_path.stem}_{sec}.json"
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump({sec: content}, jf, indent=2)

    npy_path = OUTPUT_FOLDER / f"{file_path.stem}_embedding.npy"
    np.save(npy_path, embedding)

    print(f"[OK] {file_path.name} → structured JSON + embeddings saved")

# --- MAIN ---
def main():
    txt_files = [f for f in INPUT_FOLDER.glob("*.txt")]
    if not txt_files:
        print("[WARN] No .txt resumes found.")
        return

    print(f"[INFO] Processing {len(txt_files)} resumes...")
    for f in txt_files:
        try:
            process_resume(f)
        except Exception as e:
            print(f"[ERR] {f.name}: {e}")

    print("[DONE] ✅ Resume structuring and embedding complete.")

if __name__ == "__main__":
    main()
