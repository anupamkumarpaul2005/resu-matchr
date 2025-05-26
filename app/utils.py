import fitz
import requests
from typing import List, Dict
import json
from app.prompts import ROLE_PREDICTION_PROMPT, FEEDBACK_PROMPT, JOB_MATCH_PROMPT
from app.models import Job
from app.schemas import RoleConfidence, Feedback

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"

def call_ollama(prompt: str) -> str:
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    })
    return response.json()["message"]["content"]

def get_predicted_roles(resume_text: str) -> List[RoleConfidence]:
    prompt = ROLE_PREDICTION_PROMPT.format(resume_text=resume_text)
    response = call_ollama(prompt)
    try:
        output = response.strip()
        start = output.find('[')
        end = output.rfind(']') + 1
        json_part = output[start:end]
        parsed = json.loads(json_part)
        return [RoleConfidence(**item) for item in parsed]
    except:
        return []

def get_resume_feedback(resume_text: str) -> List[Feedback]:
    prompt = FEEDBACK_PROMPT.format(resume_text=resume_text)
    response = call_ollama(prompt)
    try:
        output = response.strip()
        start = output.find('[')
        end = output.rfind(']') + 1
        output = output[start:end]
        parsed = json.loads(output)
        return [Feedback(**item) for item in parsed]
    except:
        return []

def get_job_match(resume_text: str, job: Job) -> Dict:
    prompt = JOB_MATCH_PROMPT.format(
        resume_text=resume_text,
        job_title=job.title,
        job_description=job.description,
        job_skills=job.skills,
        job_experience_level=job.experience_level,
        job_industry=job.industry,
        job_keywords=job.keywords
    )
    response = call_ollama(prompt)
    try:
        output = response.strip()
        start = output.find('{')
        end = output.rfind('}') + 1
        json_part = output[start:end]
        return json.loads(json_part)
    except:
        return {"llm_score": 0.0, "missing_skills": [], "feedback": "No feedback provided."}

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
