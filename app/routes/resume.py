from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.llm import get_predicted_roles, get_resume_feedback, get_job_match
from app.utils.parsing import extract_text_from_pdf
from app.utils.matcher import query_index
from app.db.schemas import ResumeTextInput, FeedbackResponse, ResumeTextInput, MatchResponse, JobMatchFeedback
from app.db.db import get_db
from app.db.crud import get_job

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)
    text = extract_text_from_pdf("temp_resume.pdf")
    if not text.strip():
        raise HTTPException(400, "Could not extract any text from the PDF.")
    return {"resume_text": text}

@router.post("/feedback", response_model=FeedbackResponse)
def resume_feedback(payload: ResumeTextInput):
    resume_text = payload.resume_text
    if not resume_text.strip():
        raise HTTPException(400, "Resume text cannot be empty.")
    try:
        predicted_roles = get_predicted_roles(resume_text)
        feedback = get_resume_feedback(resume_text)
        return FeedbackResponse(roles=predicted_roles, feedback=feedback)
    except Exception as e:
        raise HTTPException(500, f"Resume Feedbacking failed: {str(e)}")

@router.post("/match", response_model=MatchResponse)
def match_jobs(payload: ResumeTextInput, db: Session = Depends(get_db)):
    resume_text = payload.resume_text
    if not resume_text.strip():
        raise HTTPException(400, "Resume text cannot be empty.")
    try:
        matched_jobs = []
        jobs = query_index(resume_text, top_k=20)
        for job_id, score in jobs:
            job = get_job(job_id, db)
            if job:
                feedback = get_job_match(resume_text, job)
                matched_jobs.append(JobMatchFeedback(
                    job_id=job.id,
                    job_title=job.title,
                    faiss_score=score,
                    llm_score=feedback.get("llm_score", 0),
                    missing_skills=feedback.get("missing_skills", []),
                    feedback=feedback.get("feedback", "No feedback.")
                ))
        matched_jobs.sort(key=lambda x: x.llm_score, reverse=True)
        return MatchResponse(matches=matched_jobs[:10])
    except Exception as e:
        raise HTTPException(501, f"Job Matching failed: {str(e)}")
