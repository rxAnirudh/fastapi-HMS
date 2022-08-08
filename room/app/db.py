"""File to connect fastAPI WITH POSTGRESQL DATABASE"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import room.config

DATABASE_URL = room.config.Config.DATABASE_URL
engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()

def get_db():
    """Function to get db details"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
