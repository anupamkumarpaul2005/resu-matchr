from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime

class ResumeTextInput(BaseModel):
    resume_text: str

class JobMatchFeedback(BaseModel):
    job_id: int
    faiss_score: float
    llm_score: int
    missing_skills: List[str]
    feedback: str
    explanation: str

class MatchResponse(BaseModel):
    matches: List[JobMatchFeedback]

class RoleConfidence(BaseModel):
    role: str
    confidence: float

class Feedback(BaseModel):
    category: str
    feedback: str

class FeedbackResponse(BaseModel):
    roles: List[RoleConfidence]
    feedback: List[Feedback]

class JobResponse(BaseModel):
    title: str
    company_name: str
    location: str
    description: str
    skills: str
    job_type: str
    experience_level: str
    salary_min: int
    salary_max: int
    industry: Optional[str] = None
    keywords: Optional[str] = None
    application_link: HttpUrl
    hiring_manager_email: EmailStr
    expires_on: datetime

    class Config:
        from_attributes = True