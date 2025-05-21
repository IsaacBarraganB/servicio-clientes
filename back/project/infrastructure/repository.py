from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from project.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()