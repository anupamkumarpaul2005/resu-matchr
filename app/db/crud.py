from typing import List
from sqlalchemy.orm import Session
from app.db.models import Job
from datetime import datetime, timezone

def get_all_jobs(db: Session) -> List[Job]:
    return db.query(Job).filter(Job.expires_on > datetime.now(timezone.utc)).all()

def get_job(job_id: int, db: Session) -> Job:
    return db.get(Job, job_id)
