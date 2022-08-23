"""File for creating models of the project"""

from datetime import datetime
from operator import index
from fastapi import File
from pydantic import FilePath
from sqlalchemy import Column, TIMESTAMP, Integer,  String
from db import Base

class Payroll(Base):
    """Class for creating payroll model"""
    __tablename__ = 'payroll'

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, index=True)
    salary = Column(String, index=True)
    net_salary = Column(String, index=True)
    hourly_salary = Column(String, index=True)
    bonus_salary = Column(String, index=True)
    compensation = Column(String, index=True)
    account_no = Column(String, index=True)
    hospital_id = Column(String, index=True)
    payroll_slip = Column(String,index=True)

    
    