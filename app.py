from fastapi import FastAPI
from db.database import SessionLocal, engine,Base

"""
Create all table defined in models.py
"""
Base.metadata.create_all(bind=engine)

app = FastAPI()

"""
Dependecy
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
