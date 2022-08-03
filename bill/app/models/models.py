"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from db import Base

class Bill(Base):
    """Class for creating bill model"""
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    doctor_charge = Column(String, index=True)
    medicine_charge = Column(String, index=True)
    room_charge = Column(String, index=True)
    operation_charge = Column(String, index=True)
    no_of_days = Column(String, index=True)
    nursing_charge = Column(String, index=True)
    lab_charge = Column(Integer,index = True)
    insurance_number = Column(String, index=True)
    total_bill = Column(String, index=True)
    bill_date = Column(String,index=False)
    hospital_id = Column(String, index=True)
    
