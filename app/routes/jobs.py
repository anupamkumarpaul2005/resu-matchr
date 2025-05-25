from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import get_db
from app.models import Job
from app.matcher import add_job_to_index
from app.schemas import JobResponse
from app.crud import get_job

router = APIRouter()

@router.post("/upload")
def upload_job(
    title: str = Form(...),
    company_name: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    skills: str = Form(...),
    job_type: str = Form(...),
    experience_level: str = Form(...),
    salary_min: int = Form(...),
    salary_max: int = Form(...),
    industry: str = Form(None),
    keywords: str = Form(None),
    application_link: str = Form(...),
    hiring_manager_email: str = Form(...),
    expires_on: str = Form(...),
    db: Session = Depends(get_db)
):
    expires_dt = datetime.fromisoformat(expires_on)
    if expires_dt.tzinfo is None:
        expires_dt = expires_dt.replace(tzinfo=timezone.utc)

    new_job = Job(
        title=title,
        company_name=company_name,
        location=location,
        description=description,
        skills=skills,
        job_type=job_type,
        experience_level=experience_level,
        salary_min=salary_min,
        salary_max=salary_max,
        industry=industry,
        keywords=keywords,
        application_link=application_link,
        hiring_manager_email=hiring_manager_email,
        expires_on=expires_dt
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    combined = " ".join(filter(None, [title, description, skills, keywords, industry, experience_level]))
    add_job_to_index(new_job.id, combined)

    return {"message": "Job uploaded", "job_id": new_job.id}

@router.get("/details", response_model=JobResponse)
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    job = get_job(job_id, db)
    if not job:
        raise HTTPException(404, f"Job with ID {job_id} not found")
    return job