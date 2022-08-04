"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from db import Base

class Feedback(Base):
    """Class for creating feedback model"""
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    from_patient_id = Column(String, index=True)
    to_staff_id = Column(String, index=True)
    comment = Column(String, index=True)
    rating = Column(String, index=True)
    created_on = Column(String, index=True)
    updated_on = Column(String, index=True)
    hospital_id = Column(String, index=True)
    