"""File for creating models of the project"""

from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean
from patient_report.app.db import Base

class PatientReport(Base):
    """Class for creating patient report model"""
    __tablename__ = 'patient_report'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    report_description = Column(String, index=True)
    doctor_id = Column(String, index=True)
    hospital_id = Column(String, index=True)
    appointment_id = Column(String, index=True)

class PatientReportMedicineDetails(Base):
    """Class for creating patient report medicine details model"""
    __tablename__ = 'patient_report_medicine_details'
    patient_id = Column(String, index=True)
    medicine_id = Column(String, primary_key=True,index=True)
    