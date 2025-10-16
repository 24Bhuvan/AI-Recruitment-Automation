import re
import json
from pathlib import Path

# ===== Paths =====
INPUT_FOLDER = Path("data/processed/cleaned")
OUTPUT_FOLDER = Path("data/processed/structured")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ===== Skill keywords (extend as needed) =====
SKILL_KEYWORDS = {
    "programming": [
        "python", "java", "c++", "c#", "javascript", "typescript", "go", "rust", "php", "r"
    ],
    "data_science": [
        "machine learning", "deep learning", "nlp", "computer vision",
        "tensorflow", "pytorch", "scikit-learn", "keras", "data analysis",
        "pandas", "numpy", "matplotlib", "seaborn", "sql", "excel"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
        "terraform", "ci/cd", "linux"
    ],
    "web": [
        "html", "css", "react", "node.js", "express", "flask", "django"
    ],
    "others": [
        "git", "jira", "agile", "api", "rest", "graphql"
    ]
}

# ===== Build flat list of unique skill keywords =====
ALL_SKILLS = sorted(set(sum(SKILL_KEYWORDS.values(), [])))

def extract_skills(text: str):
    text_lower = text.lower()
    found_skills = []

    for skill in ALL_SKILLS:
        # Use word boundaries to avoid partial matches (e.g., "java" in "javascript")
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))

def process_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        skills = extract_skills(text)
        result = {"name": file_path.stem, "skills": skills}

        output_file = OUTPUT_FOLDER / f"{file_path.stem}_skills.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"[OK] {file_path.name} → {output_file.name} ({len(skills)} skills found)")

    except Exception as e:
        print(f"[ERR] {file_path.name}: {e}")

def main():
    files = [f for f in INPUT_FOLDER.iterdir() if f.is_file() and f.suffix == ".txt"]
    for file in files:
        process_file(file)

if __name__ == "__main__":
    main()
