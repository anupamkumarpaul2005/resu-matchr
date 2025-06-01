ROLE_PREDICTION_PROMPT = """
You are a career advisor and AI assistant. Based on the following resume text, predict the **top 3-5 most relevant job roles** that this candidate is best suited for **based on their skills, education, and experience**.

Guidelines:
- Only suggest realistic roles that align with the candidate's background.
- Avoid vague or overly broad roles (e.g., “Engineer”).
- Include a confidence score between 0.0 and 1.0 (rounded to 2 decimal places).
- Prefer internships or entry-level roles if the experience suggests so.

Resume Text:
{resume_text}

Return a **strict JSON array** with no other text:
[
  {{
    "role": "ML Engineer Intern",
    "confidence": 0.87
  }},
  ...
]
"""

FEEDBACK_PROMPT = """
You are a resume coach and ATS optimization expert. Review the resume text and provide 3 to 5 **actionable**, **ATS-friendly** suggestions for improvement.

Evaluate the resume on:
- Missing or unparseable contact details (e.g., phone number, email, LinkedIn)
- Improper file structure or section formatting
- Missing standard sections (e.g., Education, Skills, Experience)
- Absence of relevant technical tools, libraries, or keywords
- Weak bullet point phrasing (e.g., lack of action verbs or metrics)
- Overuse of graphics, tables, or non-text elements (if detectable)
- Text patterns that ATS may fail to parse (e.g., dates in nonstandard formats)

Resume Text:
{resume_text}

Return a **valid JSON array** only:
[
  {{
    "category": "Formatting | Missing Info | Skills | Structure | Bullet Points | ATS Parsing",
    "feedback": "Specific suggestion or issue with explanation."
  }},
  ...
]
Do not return any text before or after the JSON.
"""

JOB_MATCH_PROMPT = """
You are a career assistant and resume evaluator. Compare a resume against a job posting and provide a detailed fit analysis.

Return:
1. A **match score** between 0-100 (integer), based on skill, experience, and role alignment.
2. A list of **critical missing skills or tools** (focus on technical or role-specific).
3. Feedback to improve resume fit for this job.
4. One-line explanation for the match score (e.g., "Strong match in ML tools, but lacks NLP experience.")

Job Posting:
- Title: {job_title}
- Description: {job_description}
- Required Skills: {job_skills}
- Experience Level: {job_experience_level}
- Industry: {job_industry}
- Keywords: {job_keywords}

Resume:
{resume_text}

Return your response as valid JSON with this format:
{{
  "llm_score": ...,
  "missing_skills": ["skill1", ...],
  "feedback": "...",
  "explanation": "..."
}}
"""
