import re
from io import BytesIO
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extend this list for the job families you want to support.
SKILLS = [
    "python", "java", "c++", "sql", "mysql", "postgresql", "excel",
    "power bi", "tableau", "statistics", "machine learning", "deep learning",
    "natural language processing", "nlp", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "data analysis", "data visualization",
    "matplotlib", "seaborn", "streamlit", "flask", "fastapi", "aws",
    "azure", "git", "github", "docker", "linux", "communication",
    "problem solving", "project management", "html", "css", "javascript",
    "R", "data cleaning", "ETL", "A/B testing"
]

def extract_text(uploaded_file):
    """Extract text from a Streamlit UploadedFile (PDF, DOCX or TXT)."""
    name = uploaded_file.name.lower()
    content = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        doc = Document(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    if name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    raise ValueError("Unsupported file type. Use PDF, DOCX or TXT.")

def clean_text(text):
    """Basic NLP preprocessing: lowercase, remove URLs/emails and punctuation."""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_skills(text):
    """Find skills from a transparent, editable keyword dictionary."""
    cleaned = clean_text(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, cleaned):
            found.append(skill)
    return sorted(set(found))

def analyze_resume(resume_text, job_description, similarity_weight=0.60, skill_weight=0.40):
    """Return TF-IDF similarity, skill coverage and weighted relevance score."""
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_description)

    if not resume_clean or not job_clean:
        raise ValueError("Resume and job description must contain readable text.")
    if round(similarity_weight + skill_weight, 6) != 1:
        raise ValueError("Scoring weights must add up to 1.")

    # TF-IDF turns the two documents into numeric vectors.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform([job_clean, resume_clean])
    similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100

    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    matched = sorted(set(job_skills) & set(resume_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    coverage = (len(matched) / len(job_skills) * 100) if job_skills else 0.0

    final_score = similarity * similarity_weight + coverage * skill_weight
    return {
        "similarity": round(similarity, 2),
        "skill_coverage": round(coverage, 2),
        "final_score": round(final_score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }
