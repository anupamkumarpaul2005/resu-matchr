import streamlit as st

st.set_page_config(page_title="ResuMatchr", layout="wide")

st.title("🔍 ResuMatchr")
st.markdown("Welcome to **ResuMatchr** — a smart platform that matches resumes with jobs and gives real-time feedback!")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_User.py", label="👤 I'm a Job Seeker", icon="📄")

with col2:
    st.page_link("pages/2_Recruiter.py", label="🏢 I'm a Recruiter", icon="📢")

st.markdown("---")
st.info("Navigate using the buttons above or the sidebar on other pages.")
