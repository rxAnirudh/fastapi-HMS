"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from doctor.app.db import Base

class Doctor(Base):
    """Class for creating doctor model"""
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    contact_number = Column(String, index=True)
    profile_pic = Column(String, index=True)
    email = Column(String, index=True)
    gender = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    blood_group = Column(String, index=True)
    
class DoctorDetails(Base):
    """Class for creating doctor details model"""
    __tablename__ = 'doctor_details'
    id = Column(Integer, primary_key=True, index=True)
    years_of_experience = Column(String, index=True)
    next_available_at = Column(String,index=True)
    specialist_field = Column(String, index=True)
    education = Column(String, index=True)
    about = Column(String, index=True)
    in_clinic_appointment_fees = Column(String, index=True)
    create_at = Column(String,index=True)
    rating = Column(String,index=True)

class PatientCommentDetails(Base):
    """Class for creating patient comment details model"""
    __tablename__ = 'patient_comment_details'
    id = Column(Integer, primary_key=True, index=True)
    patients_comment = Column(String, index=True)
    user_id = Column(Integer, index=True)
    doctor_id = Column(Integer, index=True)
    