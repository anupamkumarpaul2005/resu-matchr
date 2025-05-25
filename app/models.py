from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    company_name = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    skills = Column(Text, nullable=False)
    job_type = Column(String(50), nullable=False)
    experience_level = Column(String(50), nullable=False)
    salary_min = Column(Integer, nullable=False)
    salary_max = Column(Integer, nullable=False)
    industry = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    application_link = Column(Text, nullable=False)
    hiring_manager_email = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_on = Column(DateTime(timezone=True), nullable=False)
    embedding = Column(Vector(384), nullable=True)
