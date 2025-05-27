from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List
from app.db import SessionLocal
from app.models import Job

model = SentenceTransformer('intfloat/e5-base')
index = None
job_id_map: list[int] = []

def format_resume_text(resume_text: str):
    return f"query: {resume_text}"

def format_job_text(job: Job):
    text = f""" 
    Job Title: {job.title}
    Company: {job.company_name}
    Description: {job.description}
    Required Skills: {job.skills}
    Location: {job.location}
    Keywords: {job.keywords}
    Industry: {job.industry}
    Experience Level: {job.experience_level}
    """
    return f"passage: {text}"

def init_index(jobs: List[Job], dim: int = 768):
    global index, job_id_map
    index = faiss.IndexFlatIP(dim)
    job_id_map = []
    if jobs:
        for job in jobs:
            if job.embedding is not None:
                emb = np.array(job.embedding, dtype="float32").reshape(1, -1)
                faiss.normalize_L2(emb)
                index.add(emb)
                job_id_map.append(job.id)
            else:
                add_job_to_index(job)

def add_job_to_index(job: Job):
    global index, job_id_map
    text = format_job_text(job)
    emb = model.encode([text], convert_to_numpy=True)
    faiss.normalize_L2(emb)
    index.add(emb)
    job_id_map.append(job.id)

    db = SessionLocal()
    try:
        job.embedding = emb[0].tolist()
        db.merge(job)
        db.commit()
    finally:
        db.close()

def query_index(resume_text: str, top_k: int = 5):
    query = format_resume_text(resume_text)
    emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(emb)
    scores, indices = index.search(emb, min(top_k, len(job_id_map)))
    results = []
    for rank, idx in enumerate(indices[0]):
        results.append((job_id_map[idx], float(scores[0][rank])))
    return results
