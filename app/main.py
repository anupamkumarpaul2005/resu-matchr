from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, Body
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from app.db import Base, engine, SessionLocal
from app.models import Job
from app.utils import extract_text_from_pdf, get_predicted_roles, get_resume_feedback, get_job_match
from app.crud import get_all_jobs, get_job
from app.matcher import init_index, add_job_to_index, query_index
from app.schemas import ResumeTextInput, JobMatchFeedback, MatchResponse, FeedbackResponse, JobResponse, JobIDInput


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    jobs = get_all_jobs(db)
    db.close()

    init_index(jobs)

    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)
    text = extract_text_from_pdf("temp_resume.pdf")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the PDF.")
    return {"resume_text": text}

@app.post("/upload_job")
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

    return {"message": "Job uploaded successfully", "job_id": new_job.id}


@app.post("/get_job_details", response_model=JobResponse)
def get_job_details(payload: JobIDInput, db: Session = Depends(get_db)):
    job_id = payload.job_id
    job = get_job(job_id, db)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")
    return JobResponse(
        title=job.title,
        company_name=job.company_name,
        location=job.location,
        description=job.description,
        skills=job.skills,
        job_type=job.job_type,
        experience_level=job.experience_level,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        industry=job.industry,
        keywords=job.keywords,
        application_link=job.application_link,
        hiring_manager_email=job.hiring_manager_email,
        expires_on=job.expires_on
    )


@app.post("/match_jobs_with_feedback", response_model=MatchResponse)
def match_jobs_with_feedback(payload: ResumeTextInput, db: Session = Depends(get_db)):
    global index
    resume_text = payload.resume_text
    if not resume_text.strip():
        raise HTTPException(400, "Resume text cannot be empty.")
    try:
        matched_jobs = []
        jobs = query_index(resume_text, top_k=20)
        for job_id, score in jobs:
            job = get_job(job_id, db)
            if job:
                llm_feedback = get_job_match(resume_text, job)

                matched_jobs.append(JobMatchFeedback(
                    job_id=job.id,
                    job_title=job.title,
                    faiss_score=score,
                    llm_score=llm_feedback.get("llm_score", 0),
                    missing_skills=llm_feedback.get("missing_skills", []),
                    feedback=llm_feedback.get("feedback", "No feedback provided.")
                ))
        matched_jobs.sort(key=lambda x:x.llm_score, reverse=True)

        return MatchResponse(matches=matched_jobs[:10])
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Job Matching failed: {str(e)}")

    
@app.post("/resume_feedback", response_model=FeedbackResponse)
def resume_feedback(payload:  ResumeTextInput):
    resume_text = payload.resume_text
    if not resume_text.strip():
        raise HTTPException(400, "Resume text cannot be empty.")
    try:
        predicted_roles = get_predicted_roles(resume_text)
        feedback = get_resume_feedback(resume_text)
        return FeedbackResponse(roles=predicted_roles, feedback = feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume Feedbacking failed: {str(e)}")