import os
import json
from sentence_transformers import SentenceTransformer
from pathlib import Path

# === PATHS ===
BASE_DIR = Path(r"C:\Users\B ANAND\Desktop\ai recriutment\AI-Recruitment-Automation\backend\data\processed\structured")
OUTPUT_DIR = BASE_DIR
model_name = "all-MiniLM-L6-v2"

print("[INFO] Loading model...")
model = SentenceTransformer(model_name)
print("[INFO] Model loaded successfully.\n")

# Get unique resume prefixes (e.g., resume_01, resume_02)
prefixes = sorted(set(f.name.split('_')[0] + "_" + f.name.split('_')[1] for f in BASE_DIR.glob("resume_*_skills.json")))

for prefix in prefixes:
    files = list(BASE_DIR.glob(f"{prefix}_*.json"))
    combined = {}
    text_parts = []

    for f in files:
        with open(f, "r", encoding="utf-8") as jf:
            data = json.load(jf)
            combined.update(data)
            # Collect text content for embedding
            text_parts.append(json.dumps(data, ensure_ascii=False))

    full_text = " ".join(text_parts)
    embedding = model.encode(full_text).tolist()
    combined["embedding"] = embedding

    output_file = OUTPUT_DIR / f"{prefix}.json"
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(combined, out, indent=2, ensure_ascii=False)
    
    print(f"[OK] {output_file.name} created with embedding.")

print("\n[DONE] ✅ Combined resume JSONs + embeddings saved successfully.")
