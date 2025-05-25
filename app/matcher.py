from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List
from app.db import SessionLocal
from app.crud import get_job
from app.models import Job

# --- Globals ---
model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight, fast, free
index = None
job_id_map: list[int] = []

def init_index(jobs: List[Job], dim: int = 384):
    """
    Initialize a new FAISS index for Inner-Product (cosine) search
    and reset the job_id mapping.
    """
    global index, job_id_map
    index = faiss.IndexFlatIP(dim)
    job_id_map = []
    if jobs:
        for job in jobs:
            if job.embedding is not None:
                emb = np.array(job.embedding, dtype="float32").reshape(1, -1)
                faiss.normalize_L2(emb)
                index.add(emb)
            else:
                text = " ".join(filter(None, [job.title, job.description, job.skills, job.keywords, job.industry, job.experience_level]))
                emb = model.encode([text], convert_to_numpy=True)
                faiss.normalize_L2(emb)
                index.add(emb)
            job_id_map.append(job.id)

def add_job_to_index(job_id: int, text: str):
    """
    Embed `text` and add its vector to the FAISS index,
    recording the mapping back to `job_id`.
    """
    global index, job_id_map
    emb = model.encode([text], convert_to_numpy=True)
    faiss.normalize_L2(emb)
    index.add(emb)
    job_id_map.append(job_id)

    db = SessionLocal()
    try:
        job = get_job(job_id, db)
        if job:
            job.embedding = emb[0].tolist()
            db.commit()
    finally:
        db.close()

def query_index(resume_text: str, top_k: int = 5):
    """
    Embed the resume, query the FAISS index, and return a list of
    (job_id, score) for the top_k most similar job postings.
    """
    emb = model.encode([resume_text], convert_to_numpy=True)
    faiss.normalize_L2(emb)
    scores, indices = index.search(emb, min(top_k, len(job_id_map)))
    results = []
    for rank, idx in enumerate(indices[0]):
        results.append((job_id_map[idx], float(scores[0][rank])))
    return results
