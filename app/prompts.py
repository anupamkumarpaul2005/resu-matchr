ROLE_PREDICTION_PROMPT = """
You are a career advisor. Based on the following resume text, predict the top 3-5 job roles (like Data Scientist Intern, ML Engineer, AI Research Intern, etc.) that the candidate is suited for. Provide each role with a confidence score between 0 and 1.

Resume:
{resume_text}

Return your answer as strict JSON. Do not include any text outside the JSON.
Return your answer as a JSON array like:
[
  {{"role": "...", "confidence": 0.87}},
  ...
]
"""

FEEDBACK_PROMPT = """
You are a resume coach. Based on this resume text, provide actionable feedback to improve it.

Categories:
- Missing technical skills or tools
- Suggestions for clearer structure or organization
- Bullet point improvements
- Format issues (e.g. missing sections)

Resume:
{resume_text}

Return your answer as strict JSON. Do not include any text outside the JSON.
Return a list of 3 to 5 concrete Feedbacks.
[
  {{
    "category": "...",
    "feedback": "..."
  }},
  ...
]
"""

JOB_MATCH_PROMPT = """
You are a career assistant. Given the user's resume and a job description, do the following:

1. Rate how well the resume matches the job (0 to 100).
2. List any critical missing skills.
3. Give feedback on how to improve for this role.

RESUME:
{resume_text}

JOB:
{job_title}
{job_description}
{job_skills}
{job_experience_level}
{job_industry}
{job_keywords}

Return your answer as strict JSON. Do not include any text outside the JSON.
Return a JSON like:
{{
  "llm_score": ...,
  "missing_skills": ["skill1", ...],
  "feedback": "..."
}}
"""
