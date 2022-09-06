"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import SecretStr
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from patient.app.db import Base

class Patient(Base):
    """Class for creating patient model"""
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    contact_number = Column(String, index=True)
    password = Column(String, index=True)
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
    smoking_habits = Column(String,index = True)
    alchol_consumption = Column(String,index = True)
    activity_level = Column(String,index = True)
    occupation = Column(String,index = True)

class Patient_Allergies(Base):
    """Class for creating patient allergies model"""
    __tablename__ = 'patient_allergies'
    id = Column(Integer, primary_key=True, index=True)
    allergy_id = Column(String, index=True)
    patient_id = Column(String, index=True)

class Patient_Otp_For_Password(Base):
    """Class for creating patient allergies model"""
    __tablename__ = 'patient_otp_for_password'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    otp = Column(String, index=True)
    created_at = Column(String,index=True)
    updated_at = Column(String,index=True)
    
    
class Patient_CurrentMedications(Base):
    """Class for creating patient current medications model"""
    __tablename__ = 'patient_current_medications'
    id = Column(Integer, primary_key=True, index=True)
    current_medication_id = Column(String, index=True)
    patient_id = Column(String, index=True)

class Patient_FoodPreference(Base):
    """Class for creating food preference model"""
    __tablename__ = 'patient_food_preferences'
    id = Column(Integer, primary_key=True, index=True)
    food_preference_id = Column(String, index=True)
    patient_id = Column(String, index=True)

class Patient_PastInjuries(Base):
    """Class for creating patient past injuries model"""
    __tablename__ = 'patient_past_injuries'
    id = Column(Integer, primary_key=True, index=True)
    past_injury_id = Column(String, index=True)
    patient_id = Column(String, index=True)

class Patient_PastSurgeries(Base):
    """Class for creating patient past surgeries model"""
    __tablename__ = 'patient_past_surgeries'
    id = Column(Integer, primary_key=True, index=True)
    past_surgery_id = Column(String, index=True)
    patient_id = Column(String, index=True)

class Allergies(Base):
    """Class for creating patient allergies model"""
    __tablename__ = 'allergies'
    id = Column(Integer, primary_key=True, index=True)
    allergy = Column(String, index=True)

class CurrentMedications(Base):
    """Class for creating patient current medications model"""
    __tablename__ = 'current_medications'
    id = Column(Integer, primary_key=True, index=True)
    current_medication = Column(String, index=True)

class FoodPreference(Base):
    """Class for creating food preference model"""
    __tablename__ = 'food_preferences'
    id = Column(Integer, primary_key=True, index=True)
    food_preference = Column(String, index=True)

class PastInjuries(Base):
    """Class for creating patient past injuries model"""
    __tablename__ = 'past_injuries'
    id = Column(Integer, primary_key=True, index=True)
    past_injury = Column(String, index=True)

class PastSurgeries(Base):
    """Class for creating patient past surgeries model"""
    __tablename__ = 'past_surgeries'
    id = Column(Integer, primary_key=True, index=True)
    past_surgery = Column(String, index=True)
