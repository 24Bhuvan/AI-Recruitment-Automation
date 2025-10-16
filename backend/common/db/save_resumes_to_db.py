import os
import json
import mysql.connector

# ------------------ CONFIG ------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pass123",
    "database": "airesumescreening"
}

PROCESSED_FOLDER = r"C:\Users\cssra\OneDrive\Desktop\Monarch Analytics\AI-Recruitment-Automation\data\processed\structured"
# --------------------------------------------

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Helper functions
def insert_candidate(data):
    query = """
    INSERT INTO candidates (name, dob, gender, objective, phone, email, github)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    values = (
        data.get("name"),
        data.get("dob"),
        data.get("gender"),
        data.get("objective"),
        data.get("phone"),
        data.get("email"),
        data.get("github")
    )
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid  # candidate_id

def insert_education(candidate_id, education_list):
    for edu in education_list:
        cursor.execute(
            "INSERT INTO education (candidate_id, degree, institution, year) VALUES (%s,%s,%s,%s)",
            (candidate_id, edu.get("degree"), edu.get("institution"), edu.get("year"))
        )
    conn.commit()

def insert_experience(candidate_id, experience_list):
    for exp in experience_list:
        cursor.execute(
            "INSERT INTO internships_training (candidate_id, title, organization, duration) VALUES (%s,%s,%s,%s)",
            (candidate_id, exp.get("title"), exp.get("organization"), exp.get("duration"))
        )
    conn.commit()

def insert_skills(candidate_id, skills_list):
    for skill in skills_list:
        cursor.execute(
            "INSERT INTO skills (candidate_id, skill_name) VALUES (%s,%s)",
            (candidate_id, skill)
        )
    conn.commit()

# Loop through JSON files
for filename in os.listdir(PROCESSED_FOLDER):
    if filename.endswith(".json") and "education" not in filename and "experience" not in filename:
        file_path = os.path.join(PROCESSED_FOLDER, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            resume_data = json.load(f)

        # Insert candidate
        candidate_id = insert_candidate(resume_data)

        # Insert education
        edu_file = filename.replace(".json", "_education.json")
        edu_path = os.path.join(PROCESSED_FOLDER, edu_file)
        if os.path.exists(edu_path):
            with open(edu_path, "r", encoding="utf-8") as f:
                education_list = json.load(f)
            insert_education(candidate_id, education_list)

        # Insert experience
        exp_file = filename.replace(".json", "_experience.json")
        exp_path = os.path.join(PROCESSED_FOLDER, exp_file)
        if os.path.exists(exp_path):
            with open(exp_path, "r", encoding="utf-8") as f:
                experience_list = json.load(f)
            insert_experience(candidate_id, experience_list)

        # Insert skills
        skills_list = resume_data.get("skills", [])
        insert_skills(candidate_id, skills_list)

        print(f"Processed and inserted {filename} successfully.")

# Close connection
cursor.close()
conn.close()
print("All resumes processed and database updated.")
