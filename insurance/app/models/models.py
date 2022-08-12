"""File for creating models of the project"""

from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean
from db import Base

class Insurance(Base):
    """Class for creating insurance model"""
    __tablename__ = 'insurance'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    policy_no = Column(String, index=True)
    publish_date = Column(String, index=True)
    expire_date = Column(String, index=True)
    maternity = Column(String, index=True)
    dental = Column(String, index=True)
    optical = Column(String, index=True)
    chronic_pec = Column(String, index=True)
    

class InsuranceCover(Base):
    """Class for creating insurance cover model"""
    __tablename__ = 'insurance_cover'

    id = Column(Integer, primary_key=True, index=True)
    ins_company = Column(String, index=True)
    ins_plan = Column(String, index=True)
    entry_fees = Column(String, index=True)
    co_pay = Column(String, index=True)
    co_insurance = Column(String, index=True)
    med_coverage = Column(String, index=True)
    
    
    