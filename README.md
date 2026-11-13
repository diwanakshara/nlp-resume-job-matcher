# NLP-Powered Resume Screening & Job Matching Engine

A beginner-friendly NLP project that compares PDF, DOCX and TXT resumes with a pasted job description. It calculates TF-IDF cosine similarity, detects skills from an editable skill dictionary, identifies skills not detected in each resume, ranks candidates and exports a CSV report.

## Features
- Upload multiple PDF, DOCX and TXT resumes
- Extract text from documents
- Basic text cleaning
- TF-IDF vectorization with unigrams and bigrams
- Cosine similarity between resume and job description
- Skill detection, matched-skill list and skill-gap list
- Weighted score (default: 60% text similarity + 40% skill coverage)
- Ranked results, chart and CSV download

## Project structure
```text
nlp_resume_job_matcher/
├── app.py
├── matcher.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── sample_job_description.txt
```

## Run on Windows 11
1. Install Python 3.10 or newer and VS Code.
2. Extract this ZIP and open the project folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
5. Activate it in PowerShell:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   If activation is blocked, use Command Prompt:
   ```cmd
   venv\Scripts\activate
   ```
6. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
7. Start the app:
   ```bash
   python -m streamlit run app.py
   ```
8. Open the local URL shown in the terminal (usually http://localhost:8501).

## How the score works
- **TF-IDF similarity:** represents resume and job-description text as weighted word/phrase vectors.
- **Cosine similarity:** measures the angle-based similarity of those vectors.
- **Skill coverage:** matched skills divided by all detected skills in the job description, multiplied by 100.
- **Final score:** `(similarity × similarity_weight) + (skill_coverage × skill_weight)`.

The default weights are 60% similarity and 40% skill coverage. You can change them in the sidebar.

## Customize skills
Open `matcher.py` and edit the `SKILLS` list. Add relevant technical and professional skills for your target roles. Skill detection is dictionary/keyword-based, so it may miss synonyms or context.

## Important limitations and responsible use
- A match score is a measure of textual relevance, not hiring probability, candidate quality or proof of skill.
- Skill detection only checks the editable keyword list; it does not verify proficiency.
- TF-IDF is lexical and may miss meaning when candidates use different wording.
- Image-only/scanned PDFs need OCR; this version extracts embedded text only.
- Do not use this demo to automatically reject candidates. Human review, structured interviews and job-related assessments are essential.
- For real candidate data, obtain consent and implement access controls, encryption, retention/deletion policies and bias testing before deployment.

## Suggested upgrades
1. Add OCR for scanned PDFs.
2. Add spaCy named-entity recognition for names, organizations and education.
3. Replace/compare TF-IDF with Sentence Transformers embeddings.
4. Add SQLite/PostgreSQL for job and candidate records.
5. Add evaluation using labelled resume/job pairs and ranking metrics such as Precision@K.
6. Add tests and deploy only after privacy and fairness review.
