import streamlit as st
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

st.set_page_config(page_title="ResuMatchr", layout="centered")

default_states = {
    "resume_uploaded": False,
    "resume_text": "",
    "actions_triggered": False,
    "last_resume": None
}
for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value


def is_valid_resume(text: str) -> bool:
    resume_markers = [
        "education", "experience", "skill", "project", "certification",
        "linkedin", "github"
    ]
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_pattern = r"(\+?\d{1,3})?\s?-?\(?\d{3,4}\)?[-\s]?\d{3}[-\s]?\d{4}"

    hits = 0
    if re.search(email_pattern, text): hits += 1
    if re.search(phone_pattern, text): hits += 1
    for word in resume_markers:
        if word in text.lower():
            hits+=1
    return hits > 3

st.header("📄 Upload Your Resume")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

upload_btn = st.button("📤 Upload & Analyze Resume", disabled=uploaded_resume is None)

if uploaded_resume != st.session_state.last_resume:
    for key in default_states:
        st.session_state[key] = default_states[key]
    st.session_state.last_resume = uploaded_resume

if upload_btn:
    if uploaded_resume:
        with st.spinner("🔍 Extracting text from resume..."):
            try:
                resp = requests.post(
                    f"http://{FASTAPI_URL}/resume/upload",
                    files={"file": (uploaded_resume.name, uploaded_resume, "application/pdf")}
                )
                resp.raise_for_status()
                st.session_state.resume_uploaded = True
                st.session_state.resume_text = resp.json().get("resume_text", "")
                if not is_valid_resume(st.session_state.resume_text):
                    st.error("The PDF file doesn't pass as a Resume!!")
                    st.session_state.actions_triggered = False
                else:
                    st.session_state.actions_triggered = True
            except Exception as e:
                st.error(f"❌ Extraction failed: {e}")
    else:
        st.warning("Please upload a PDF file.")

if not uploaded_resume:
    for key in default_states:
        st.session_state[key] = default_states[key]

if st.session_state.resume_uploaded:
    st.subheader("📝 Extracted Resume Text")
    with st.expander("📄 View Resume Text"):
        st.text(st.session_state.resume_text[:3000])

if st.session_state.actions_triggered:
    
    with st.spinner("⚙️ Generating feedback..."):
        try:
            feedback_resp = requests.post(
                f"http://{FASTAPI_URL}/resume/feedback",
                json={"resume_text": st.session_state.resume_text}
            )
            feedback_resp.raise_for_status()
            feedback_data = feedback_resp.json()

            st.subheader("🛠️ Resume Feedback")

            st.markdown("**🎯 Predicted Job Roles:**")
            for role in feedback_data["roles"]:
                st.markdown(f"- **{role['role']}** ({role['confidence']:.0%})")
            st.markdown("**🔧 Improvement Suggestions:**")
            for sugg in feedback_data["feedback"]:
                st.markdown(f"- **{sugg['category']}:** {sugg['feedback']}")
        except Exception as e:
            st.error(f"🚨 Analysis failed: {e}")

    with st.spinner("🔍 Matching with jobs..."):
        try:
            match_resp = requests.post(
                f"http://{FASTAPI_URL}/resume/match",
                json={
                    "resume_text": st.session_state.resume_text,
                    "roles": feedback_data["roles"]
                }
            )
            match_resp.raise_for_status()
            matches = match_resp.json().get("matches", [])

            st.subheader("📌 Top Job Matches")
            if not matches:
                st.info("No matches found.")
            for match in matches:
                job = requests.get(
                    f"http://{FASTAPI_URL}/job/details?job_id={match['job_id']}"
                ).json()

                st.markdown(f"### 💼 {job['title']} — {job['company_name']}")
                st.write(f"**Match Score:** {match['match_score']:.2f}")
                st.write(f"**Missing Skills:** {', '.join(match['missing_skills']) or 'None'}")
                st.write(f"**Feedback:** {match['feedback']}")
                st.write(f"**Why this job?** {match['explanation']}")

                with st.expander("📋 Job Details"):
                    st.write(f"- **Location:** {job['location']}")
                    st.write(f"- **Type:** {job['job_type']}")
                    st.write(f"- **Experience:** {job['experience_level']}")
                    st.write(f"- **Industry:** {job.get('industry', '—')}")
                    st.write(f"- **Salary:** ₹{job['salary_min']:,}–₹{job['salary_max']:,}")
                    st.write(f"- **Apply:** [Application Link]({job['application_link']})")
                    st.write(f"- **Expires On:** {job['expires_on']}")
                    st.write("**Job Description:**")
                    st.write(job["description"])
                st.markdown("---")

        except Exception as e:
            st.error(f"🚨 Matching failed: {e}")
