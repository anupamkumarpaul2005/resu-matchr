ROLE_PREDICTION_PROMPT = """
You are a career advisor and AI assistant. Based on the following resume text extracted as Markdown from a pdf file, predict the **top 3-5 job roles** the candidate is realistically suited for based on their **skills, education, and experience**.

Guidelines:
- Only return roles the candidate is clearly prepared for.
- Do not suggest vague or broad titles like "Engineer" or "Developer".
- If the candidate has limited experience, prioritize internships or entry-level roles.
- Be strict and professional—do not overestimate.
- Each role must include a confidence score (0.0-1.0), rounded to 2 decimal places.
- If the input does not appear to be a resume (i.e., lacks relevant job history, skills, education, etc.), return an empty list `[]` and no explanation.

Resume Markdown:
{resume_text}

Return a strict JSON array only, without any additional commentary:
Do not change the name of variables.
[
  {{
    "role": "ML Engineer Intern",
    "confidence": 0.87
  }},
  ...
]
"""

FEEDBACK_PROMPT = """
You are a resume coach and ATS (Applicant Tracking System) optimization expert. Review the resume text extracted as Markdown from a pdf file and give **4 to 5 actionable, concise suggestions** for improvement.

Strict Requirements:
- Be direct. Do not praise the resume or add fluff.
- Make suggestions ATS-friendly and professional.
- Avoid repetition or vague advice.
- If the input does not appear to be a resume (i.e., lacks relevant job history, skills, education, etc.), return an empty list `[]` and no explanation.

Evaluate the resume on:
- Missing or unparseable contact info (phone, email, LinkedIn)
- Improper or inconsistent section formatting
- Missing standard sections (e.g., Education, Skills, Experience)
- Absence of key technical tools, libraries, or keywords based on content
- Weak or vague bullet points (missing action verbs, metrics, or clarity)
- Use of non-ATS-friendly patterns (e.g., images, tables, odd date formats)

Resume Markdown:
{resume_text}

Return a strict JSON array like this:
Do not change the name of variables.
[
  {{
    "category": "Formatting | Missing Info | Skills | Structure | Bullet Points | ATS Parsing",
    "feedback": "Specific, direct suggestion or issue."
  }},
  ...
]
"""

JOB_MATCH_PROMPT = """
You are a career assistant and resume evaluator. Compare the resume extracted as Markdown from a pdf file against the job description and return a detailed fit analysis.

Return:
1. A match score (0-100) based on skills, experience, and role fit.
2. Decode the skills necessary for the jobs and the skills in the resume, and find the skills that are lacking in resume. List all the missing skills.
3. Specific, no-fluff feedback to improve the resume for this job.
4. A one-line explanation of the match score rationale.

Scoring Rules:
- Penalize if the resume experience does not meet the job's level.
- If resume is unrelated (e.g., marketing resume for IT job), return a match_score of -1 and note invalid match.
- Only score highly if both experience **and** skills match.
- Avoid scores always in the 60-85 range — be honest and strict.
- If the job is related to the LLM predicted Roles, then reward them, else penalise them.

Scoring Guidelines:
- 90-100: Strong, nearly perfect match.
- 75-89: Good match with minor gaps.
- 50-74: Moderate match; lacks key areas or experience.
- 25-49: Weak match; mismatched role or many gaps.
- 0-24: Poor match; resume clearly unrelated.
- -1: Invalid input or not a resume.

Important: If the job requires a **Mid-level** or **Senior-level** experience and the resume only includes **internships or college projects**, reduce the score accordingly and mention this in the feedback.

Job Posting:
- Title: {job_title}
- Description: {job_description}
- Required Skills: {job_skills}
- Experience Level: {job_experience_level}
- Industry: {job_industry}
- Keywords: {job_keywords}

Resume Markdown:
{resume_text}

LLM Predicted Roles:
{roles}

Return your response as strict JSON:
Do not change the name of variables.
{{
  "match_score": ...,
  "missing_skills": ["skill1", ...],
  "feedback": "...",
  "explanation": "..."
}}
"""
