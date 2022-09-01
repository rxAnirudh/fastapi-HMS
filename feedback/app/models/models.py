"""File for creating models of the project"""

from sqlalchemy import Column, Integer,  String
from db import Base

class Feedback(Base):
    """Class for creating feedback model"""
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    staff_id = Column(String, index=True)
    doctor_id = Column(String, index=True)
    created_on = Column(String, index=True)
    updated_on = Column(String, index=True)
    hospital_id = Column(String, index=True)
    