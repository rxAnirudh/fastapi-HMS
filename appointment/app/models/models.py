"""File for creating models of the project"""

from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean
from db import Base

class Appointment(Base):
    """Class for creating appointment model"""
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    hospital_id = Column(String, index=True)
    staff_id = Column(String, index=True)
    start_time = Column(String, index=True)
    end_time = Column(String, index=True)
    status_id = Column(String, index=True)
    booking_time = Column(String, index=True)

class AppointmentStatus(Base):
    """Class for creating appointment status model"""
    __tablename__ = 'appointment_status'

    a_id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    