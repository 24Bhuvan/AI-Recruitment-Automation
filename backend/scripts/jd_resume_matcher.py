# jd_resume_matcher.py
import json
from pathlib import Path
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# -------- PATHS --------
BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_STRUCTURED = BASE_DIR / "data/processed/structured"
JD_STRUCTURED = BASE_DIR / "data/jd/structured"
OUTPUT_FILE = BASE_DIR / "data/match_results.json"

# -------- HELPERS --------
def load_embeddings(folder):
    embeddings = {}
    if not folder.exists():
        print(f"[ERROR] Folder not found: {folder}")
        return embeddings

    for file in folder.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "embedding" in data:
                    embeddings[file.stem] = np.array(data["embedding"])
        except Exception as e:
            print(f"[WARN] {file.name}: {e}")
    return embeddings

# -------- MAIN --------
def main():
    print(f"[INFO] Loading resume embeddings from: {RESUME_STRUCTURED}")
    resumes = load_embeddings(RESUME_STRUCTURED)
    print(f"[INFO] Loaded {len(resumes)} resume embeddings.")

    print(f"[INFO] Loading JD embeddings from: {JD_STRUCTURED}")
    jds = load_embeddings(JD_STRUCTURED)
    print(f"[INFO] Loaded {len(jds)} JD embeddings.")

    if not resumes or not jds:
        print("[ERROR] Missing embeddings. Ensure JSON structured files with 'embedding' exist in both folders.")
        return

    results = {}
    for jd_name, jd_emb in jds.items():
        jd_emb = jd_emb.reshape(1, -1)
        similarities = {}
        for res_name, res_emb in resumes.items():
            sim = cosine_similarity(jd_emb, res_emb.reshape(1, -1))[0][0]
            similarities[res_name] = float(sim)
        top_matches = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:5]
        results[jd_name] = top_matches
        print(f"[OK] {jd_name}: Top matches → {[m[0] for m in top_matches]}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"[DONE] ✅ Matching complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
