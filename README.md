# Resume Screening Project

## Setup & Usage

Follow these steps to process resumes and insert data into the database:

1. Create & activate a virtual environment.
2. Install dependencies.
3. Ensure MySQL is running and the `airesumescreening` schema is loaded.
4. Place raw resumes into `data/raw/`.
5. Run `backend/services/resume_service/resume_parser.py`.
6. Run `backend/services/resume_service/text_cleaner.py`.
7. Run `backend/services/resume_service/education_extractor.py`.
8. Run `backend/services/resume_service/experience_extractor.py`.
9. Run `backend/services/resume_service/skill_extractor.py`.
10. Inspect `data/processed/structured/` for the JSON files.
11. Run `backend/common/db/connection.py` to verify DB connectivity.  
   *It should print:* `Connected to database: airesumescreening`
12. Run `backend/common/db/save_resumes_to_db.py` to insert data into the database.

> **Note:** If `connection.py` fails, fix credentials, DB, or server before proceeding to step 12.
