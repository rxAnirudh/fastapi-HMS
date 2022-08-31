"""File for creating models of the project"""

from datetime import datetime
from operator import index
from pydantic import validator
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from hospital.app.db import Base


class Hospital(Base):
    """Class for creating hospital model"""
    __tablename__ = 'hospital'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    city = Column(String, index=True)
    pincode = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)
    
class HospitalDetails(Base):
    """Class for creating hospital details model"""
    __tablename__ = 'hospital_details'
    id = Column(Integer, primary_key=True, index=True)
    hospital_type = Column(String, index=True)
    is_rented = Column(String, index=True)
    contact_number = Column(String, index=True)
    email = Column(String, index=True)
    create_at = Column(TIMESTAMP,default=datetime.utcnow)
