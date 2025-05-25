import streamlit as st
import requests

# Session state initialization
for key, default in {
    "resume_uploaded": False,
    "resume_text": "",
    "feedback_requested": False,
    "match_requested": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.header("📄 Upload Your Resume")

# Upload resume
col1, col2 = st.columns(2)
with col1:
    uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
with col2:
    disabled = uploaded_resume is None
    if st.button("📤 Upload Resume", disabled=disabled):
        if uploaded_resume:
            try:
                resp = requests.post(
                    "http://localhost:8000/resume/upload",
                    files={"file": (uploaded_resume.name, uploaded_resume, "application/pdf")}
                )
                resp.raise_for_status()
                st.session_state.resume_uploaded = True
                st.session_state.resume_text = resp.json().get("resume_text", "")
            except Exception as e:
                st.error(f"Upload failed: {e}")

# Show resume text & actions
if st.session_state.resume_uploaded:
    st.subheader("Extracted Resume Text")
    with st.expander("View Resume Text"):
        st.text(st.session_state.resume_text[:3000])

    b1, b2 = st.columns(2)
    with b1:
        if st.button("🛠️ Get Resume Feedback"):
            st.session_state.feedback_requested = True
    with b2:
        if st.button("🔍 Match with Jobs"):
            st.session_state.match_requested = True

# Resume feedback
if st.session_state.feedback_requested:
    with st.spinner("Analyzing your resume..."):
        try:
            resp = requests.post(
                "http://localhost:8000/resume/feedback",
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

# Job matches
if st.session_state.match_requested:
    with st.spinner("Matching your resume with jobs..."):
        try:
            resp = requests.post(
                "http://localhost:8000/resume/match",
                json={"resume_text": st.session_state.resume_text}
            )
            resp.raise_for_status()
            matches = resp.json().get("matches", [])

            st.subheader("🔍 Top Job Matches")
            if not matches:
                st.info("No matches found.")
            for match in matches:
                job = requests.get(
                    f"http://localhost:8000/job/details?job_id={match['job_id']}"
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
