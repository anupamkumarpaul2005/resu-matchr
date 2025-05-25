import streamlit as st
from datetime import datetime, timedelta
import requests

# ── 1. Initialize session state ────────────────────────────────────────────────
for key, default in {
    "resume_uploaded": False,
    "resume_text": "",
    "feedback_requested": False,
    "match_requested": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── 2. Page config & title ────────────────────────────────────────────────────
st.set_page_config(page_title="ResuMatchr", layout="wide")
st.title("🔍 ResuMatchr")

# ── 3. Sidebar role selector ──────────────────────────────────────────────────
option = st.sidebar.selectbox("Choose role", ["User (Job Seeker)", "Recruiter"])

# ── 4. User (Job Seeker) Flow ─────────────────────────────────────────────────
if option == "User (Job Seeker)":
    st.header("📄 Upload Your Resume")

    # — Upload controls —
    col1, col2 = st.columns(2)
    with col1:
        uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
    with col2:
        disabled = uploaded_resume is None
        if st.button("📤 Upload Resume", disabled=disabled):
            if uploaded_resume:
                try:
                    resp = requests.post(
                        "http://localhost:8000/upload_resume",
                        files={"file": (uploaded_resume.name, uploaded_resume, "application/pdf")}
                    )
                    resp.raise_for_status()
                    st.session_state.resume_uploaded = True
                    st.session_state.resume_text = resp.json().get("resume_text", "")
                except Exception as e:
                    st.error(f"Upload failed: {e}")

    # — Show extracted text & action buttons —
    if st.session_state.resume_uploaded:
        st.subheader("Extracted Resume Text")
        with st.expander("View Resume Text"):
            st.text(st.session_state.resume_text[:3000])

        # Action buttons in columns
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🛠️ Get Resume Feedback"):
                st.session_state.feedback_requested = True
        with b2:
            if st.button("🔍 Match with Jobs"):
                st.session_state.match_requested = True

    # — Show feedback —
    if st.session_state.feedback_requested:
        with st.spinner("Analyzing your resume..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/resume_feedback",
                    json={"resume_text": st.session_state.resume_text}
                )
                resp.raise_for_status()
                data = resp.json()

                st.subheader("🔍 Predicted Job Roles")
                for item in data["roles"]:
                    st.markdown(f"- **{item['role']}** ({item['confidence']:.0%})")

                st.subheader("🛠️ Resume Improvement Suggestions")
                for sugg in data["feedback"]:
                    st.markdown(f"- **{sugg['category']}:** {sugg['feedback']}")

            except Exception as e:
                st.error(f"Feedback request failed: {e}")

    # — Show matches —
    if st.session_state.match_requested:
        with st.spinner("Matching your resume with jobs..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/match_jobs_with_feedback",
                    json={"resume_text": st.session_state.resume_text}
                )
                resp.raise_for_status()
                matches = resp.json().get("matches", [])

                st.subheader("🔍 Top Job Matches")
                if not matches:
                    st.info("No matches found.")
                for match in matches:
                    # Fetch full job details
                    job = requests.post(
                        "http://localhost:8000/get_job_details",
                        json={"job_id": match["job_id"]}
                    ).json()

                    st.markdown(f"### {job['title']} — {job['company_name']}  ")
                    st.write(f"**Faiss Score:** {match['faiss_score']:.4f}  ")
                    st.write(f"**LLM Score:** {match['llm_score']}  ")
                    st.write(f"**Missing Skills:** {', '.join(match['missing_skills']) or 'None'}  ")
                    st.write(f"**Feedback:** {match['feedback']}  ")

                    with st.expander("More Details"):
                        st.write(f"- **Location:** {job['location']}")
                        st.write(f"- **Type:** {job['job_type']}")
                        st.write(f"- **Experience:** {job['experience_level']}")
                        st.write(f"- **Industry:** {job.get('industry','—')}")
                        st.write(f"- **Salary:** ₹{job['salary_min']:,}–₹{job['salary_max']:,}")
                        st.write(f"- **Apply:** [Link]({job['application_link']})")
                        st.write(f"- **Expires on:** {job['expires_on']}")
                        st.write("**Description:**")
                        st.write(job["description"])
                    st.markdown("---")

            except Exception as e:
                st.error(f"Match request failed: {e}")


# ── 5. Recruiter Flow ───────────────────────────────────────────────────────────
else:
    st.header("📢 Post a Job Opening")
    with st.form("job_form"):
        title = st.text_input("🔖 Job Title *")
        company = st.text_input("🏢 Company Name *")
        location = st.text_input("📍 Location *")
        job_type = st.selectbox("💼 Job Type *",
            ["Full-time","Part-time","Contract","Remote","Hybrid","Internship","Other"])
        exp_lvl = st.selectbox("📊 Experience Level *",
            ["Intern","Entry","Mid","Senior","Other"])
        industry = st.text_input("🏭 Industry")
        desc = st.text_area("📝 Description *", height=200)
        skills = st.text_input("🧠 Required Skills * (comma-separated)")
        salary_min, salary_max = st.slider(
            "💰 Salary Range (₹)", 0, 300000, (30000,120000), step=5000)
        link = st.text_input("🔗 Application Link *")
        email = st.text_input("📧 Hiring Manager Email *")
        deadline = st.date_input(
            "📅 Deadline *", min_value=datetime.today()+timedelta(days=1))
        submitted = st.form_submit_button("✅ Submit Job")

        if submitted:
            if not (title and company and location and desc and skills and link and email):
                st.error("Please fill in all required fields.")
            else:
                payload = {
                    "title": title,
                    "company_name": company,
                    "location": location,
                    "job_type": job_type,
                    "experience_level": exp_lvl,
                    "industry": industry,
                    "description": desc,
                    "skills": skills,
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "application_link": link,
                    "hiring_manager_email": email,
                    "expires_on": (deadline.isoformat()),
                }
                try:
                    resp = requests.post("http://localhost:8000/upload_job", data=payload)
                    resp.raise_for_status()
                    st.success(f"Job posted! ID: {resp.json().get('job_id')}")
                except Exception as e:
                    st.error(f"Job post failed: {e}")
