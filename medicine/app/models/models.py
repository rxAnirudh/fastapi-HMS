"""File for creating models of the project"""

from operator import index
from fastapi import File
from sqlalchemy import Column, Integer,  String
from medicine.app.db import Base

class Medicine(Base):
    """Class for creating medicine model"""
    __tablename__ = 'medicine'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    cost = Column(String, index=True)
    description = Column(String, index=True)
    
class MedicineReport(Base):
    """Class for creating medicine details model"""
    __tablename__ = 'medicine_report'
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String,index = True)
    quantity = Column(String, index=True)
    production_date = Column(String,index = True)
    expire_date = Column(String, index=True)
    country = Column(String,index = True)
    supplier_id = Column(String, index=True)
