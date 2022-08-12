"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from db import Base

class Lab(Base):
    """Class for creating lab model"""
    __tablename__ = 'lab'

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    hospital_id = Column(String, index=True)
    test_type = Column(String, index=True)
    test_code = Column(String, index=True)
    weight = Column(String, index=True)
    height = Column(String, index=True)
    blood_pressure = Column(String, index=True)
    test_result = Column(String,index = True)
    created_at = Column(String, index=True)
    updated_at = Column(String, index=True)
