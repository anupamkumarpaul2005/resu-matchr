from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.llm import get_predicted_roles, get_resume_feedback, get_job_match
from app.utils.parsing import extract_text_from_pdf
from app.utils.matcher import query_index
from app.db.schemas import ResumeTextInput, FeedbackResponse, MatchInput, MatchResponse, JobMatchFeedback
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
def match_jobs(payload: MatchInput, db: Session = Depends(get_db)):
    resume_text = payload.resume_text
    roles = str(payload.roles)
    if not resume_text.strip():
        raise HTTPException(400, "Resume text cannot be empty.")
    try:
        matched_jobs = []
        jobs = query_index(resume_text, top_k=10)
        for job_id, faiss_score in jobs:
            job = get_job(job_id, db)
            if job:
                feedback = get_job_match(resume_text, roles, job)
                if feedback.get("match_score",0) > 0:
                    score = min(feedback.get("match_score",0)*1.2*faiss_score, 100)
                    matched_jobs.append(JobMatchFeedback(
                        job_id=job.id,
                        job_title=job.title,
                        match_score=score,
                        missing_skills=feedback.get("missing_skills", []),
                        feedback=feedback.get("feedback", "No feedback."),
                        explanation=feedback.get("explanation", "No  explanation provided.")
                    ))
        matched_jobs.sort(key=lambda x: x.match_score, reverse=True)
        return MatchResponse(matches=matched_jobs[:5])
    except Exception as e:
        raise HTTPException(501, f"Job Matching failed: {str(e)}")
