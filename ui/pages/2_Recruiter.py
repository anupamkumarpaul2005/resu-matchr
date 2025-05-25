import streamlit as st
from datetime import datetime, timedelta
import requests

# Sidebar navigation
st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/1_User.py", label="👤 User", icon="📄")
st.sidebar.page_link("pages/2_Recruiter.py", label="🏢 Recruiter", icon="📢")

st.header("📢 Post a Job Opening")

with st.form("job_form"):
    title = st.text_input("🔖 Job Title *")
    company = st.text_input("🏢 Company Name *")
    location = st.text_input("📍 Location *")
    job_type = st.selectbox("💼 Job Type *", ["Full-time", "Part-time", "Contract", "Remote", "Hybrid", "Internship", "Other"])
    exp_lvl = st.selectbox("📊 Experience Level *", ["Intern", "Entry", "Mid", "Senior", "Other"])
    industry = st.text_input("🏭 Industry")
    desc = st.text_area("📝 Description *", height=200)
    skills = st.text_input("🧠 Required Skills * (comma-separated)")
    salary_min, salary_max = st.slider("💰 Salary Range (₹)", 0, 300000, (30000, 120000), step=5000)
    link = st.text_input("🔗 Application Link *")
    email = st.text_input("📧 Hiring Manager Email *")
    deadline = st.date_input("📅 Deadline *", min_value=datetime.today() + timedelta(days=1))
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
                "expires_on": deadline.isoformat(),
            }
            try:
                resp = requests.post("http://localhost:8000/upload_job", data=payload)
                resp.raise_for_status()
                st.success(f"Job posted! ID: {resp.json().get('job_id')}")
            except Exception as e:
                st.error(f"Job post failed: {e}")
