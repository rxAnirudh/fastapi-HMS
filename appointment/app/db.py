"""File to connect fastAPI WITH POSTGRESQL DATABASE"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import appointment.config

DATABASE_URL = appointment.config.Config.DATABASE_URL
appointment_engine = create_engine(url='postgresql://anirudh.chawla:123@localhost/appointment',)

SessionLocal = sessionmaker(bind=appointment_engine,autocommit=False,autoflush=False,expire_on_commit=False)

Base = declarative_base()

def get_db():
    """Function to get db details"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
