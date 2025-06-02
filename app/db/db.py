from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_DB = os.getenv("DATABASE_DB")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_DB}")

with engine.connect() as connection:
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    connection.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()