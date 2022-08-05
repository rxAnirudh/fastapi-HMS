"""File for creating models of the project"""

from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean
from db import Base

class PatientReport(Base):
    """Class for creating patient report model"""
    __tablename__ = 'patient_report'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    report_id = Column(String, index=True)
    diagnose = Column(String, index=True)
    reference = Column(String, index=True)
    medicine_id = Column(String, index=True)
    medicine_name = Column(String, index=True)
    doctor_id = Column(String, index=True)
    hospital_id = Column(String, index=True)
    patient_report_file = Column(String,index=True)
    