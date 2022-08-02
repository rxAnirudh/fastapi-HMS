"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from db import Base

class Staff(Base):
    """Class for creating staff model"""
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    contact_number = Column(String, index=True)
    profile_pic = Column(String, index=True)
    email = Column(String, index=True)
    gender = Column(String, index=True)
    date_of_birth = Column(String, index=True)
    blood_group = Column(String, index=True)
    hospital_id = Column(Integer,index = True)
    
class StaffDetails(Base):
    """Class for creating staff details model"""
    __tablename__ = 'staff_details'
    id = Column(Integer, primary_key=True, index=True)
    years_of_experience = Column(String, index=True)
    education = Column(String, index=True)
    create_at = Column(String,index=True)


    