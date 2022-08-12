"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from db import Base

class Patient(Base):
    """Class for creating patient model"""
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    contact_number = Column(String, index=True)
    profile_pic = Column(String, index=True)
    email = Column(String, index=True)
    gender = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    hospital_id = Column(Integer,index = True)
    blood_group = Column(String, index=True)
    
class PatientDetails(Base):
    """Class for creating patient details model"""
    __tablename__ = 'patient_details'
    id = Column(Integer, primary_key=True, index=True)
    marital_status = Column(String,index = True)
    height = Column(String, index=True)
    weight = Column(String,index = True)
    emergency_contact_number = Column(String, index=True)
    city = Column(String,index = True)
    allergies = Column(String, index=True)
    current_medications = Column(String,index = True)
    past_injuries = Column(String,index = True)
    past_surgeries = Column(String,index = True)
    smoking_habits = Column(String,index = True)
    alchol_consumption = Column(String,index = True)
    activity_level = Column(String,index = True)
    food_preference = Column(String,index = True)
    occupation = Column(String,index = True)
