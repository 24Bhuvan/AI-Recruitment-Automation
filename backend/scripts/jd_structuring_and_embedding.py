import os
import json
from sentence_transformers import SentenceTransformer

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_FOLDER = os.path.join(BASE_DIR, "data", "jd", "cleaned")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "data", "jd", "structured")

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("[INFO] Loading model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("[INFO] Model loaded successfully.")

# Check if cleaned JD folder exists
if not os.path.exists(RAW_FOLDER):
    print(f"[ERROR] JD cleaned folder not found: {RAW_FOLDER}")
    exit(1)

files = [f for f in os.listdir(RAW_FOLDER) if f.endswith(".txt")]
if not files:
    print(f"[WARN] No .txt files found in {RAW_FOLDER}")
    exit(0)

print(f"[INFO] Processing {len(files)} job description(s)...")

for file in files:
    file_path = os.path.join(RAW_FOLDER, file)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Basic structuring
    structured_data = {
        "filename": file,
        "content": text,
        "embedding": model.encode(text).tolist()
    }

    # Save structured JSON
    output_path = os.path.join(OUTPUT_FOLDER, file.replace(".txt", ".json"))
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(structured_data, out, ensure_ascii=False, indent=4)

    print(f"[OK] {file} → structured JSON + embeddings saved")

print("[DONE] ✅ JD structuring and embedding complete.")
