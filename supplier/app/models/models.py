"""File for creating models of the project"""

from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean
from db import Base

class Supplier(Base):
    """Class for creating supplier model"""
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    contact_number = Column(String, index=True)
    email_id = Column(String, index=True)
    address = Column(String, index=True)
    
    