
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, 
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} # sqlite connect er jonno eita lagbe
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# dependency (FastAPI use)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
