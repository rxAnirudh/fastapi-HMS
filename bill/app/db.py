"""File to connect fastAPI WITH POSTGRESQL DATABASE"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



from config import Config

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(url="postgresql://anirudh.chawla:123@localhost/hospital_management")

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()