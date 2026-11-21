import streamlit as st
import pandas as pd
from matcher import analyze_resume, extract_text

st.set_page_config(page_title="NLP Resume & Job Matcher", page_icon="📄", layout="wide")
st.title("📄 NLP-Powered Resume Screening & Job Matching Engine")
st.caption("Upload resumes, paste a job description, and compare candidates using NLP and skill coverage.")

with st.sidebar:
    st.header("Scoring settings")
    similarity_weight = st.slider("Text similarity weight (%)", 0, 100, 60)
    skill_weight = 100 - similarity_weight
    st.write(f"Skill coverage weight: **{skill_weight}%**")
    st.info("Scores indicate textual relevance only. They are not hiring decisions or proof of candidate ability.")

job_description = st.text_area(
    "Paste the job description",
    height=220,
    placeholder="Example: We are looking for a Data Analyst with Python, SQL, Excel, Power BI, statistics and communication skills..."
)

uploads = st.file_uploader(
    "Upload resumes (PDF, DOCX or TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if st.button("Analyze resumes", type="primary", disabled=not job_description.strip() or not uploads):
    rows = []
    with st.spinner("Reading and comparing resumes..."):
        for uploaded in uploads:
            try:
                resume_text = extract_text(uploaded)
                if not resume_text.strip():
                    st.warning(f"No readable text found in {uploaded.name}. Scanned PDFs may need OCR.")
                    continue
                result = analyze_resume(
                    resume_text,
                    job_description,
                    similarity_weight / 100,
                    skill_weight / 100
                ) 
                rows.append({
                    "Resume": uploaded.name,
                    "Match score (%)": result["final_score"],
                    "Text similarity (%)": result["similarity"],
                    "Skill coverage (%)": result["skill_coverage"],
                    "Matched skills": ", ".join(result["matched_skills"]) or "None detected",
                    "Missing skills": ", ".join(result["missing_skills"]) or "None detected",
                })
            except Exception as exc:
                st.error(f"Could not process {uploaded.name}: {exc}")

    if rows:
        results = pd.DataFrame(rows).sort_values("Match score (%)", ascending=False).reset_index(drop=True)
        results.insert(0, "Rank", range(1, len(results) + 1))
        st.subheader("Ranked candidates")
        st.dataframe(results, use_container_width=True, hide_index=True)
        st.bar_chart(results.set_index("Resume")[["Match score (%)", "Text similarity (%)", "Skill coverage (%)"]])
        csv = results.to_csv(index=False).encode("utf-8")
        st.download_button("Download results as CSV", csv, "resume_matching_results.csv", "text/csv")
        st.subheader("Candidate skill-gap details")
        for _, row in results.iterrows():
            with st.expander(f"#{row['Rank']} — {row['Resume']} ({row['Match score (%)']}%)"):
                st.write("**Matched skills:**", row["Matched skills"])
                st.write("**Skills not detected:**", row["Missing skills"])
    else:
        st.warning("No readable resumes were processed.")

st.divider()
st.caption("Privacy: this demo processes uploaded files during the app session. Do not upload confidential resumes to a public deployment without appropriate consent, security and retention controls.")
