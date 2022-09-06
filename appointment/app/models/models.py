"""File for creating models of the project"""

import re
from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean,ARRAY
from appointment.app.db import Base
from pydantic import validator

class Appointment(Base):
    """Class for creating appointment model"""
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    doctor_id = Column(String, index=True)
    hospital_id = Column(String, index=True)
    staff_id = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    mobile_number = Column(String, index=True)
    patient_profile_pic = Column(String, index=True)
    disease = Column(String, index=True)
    status_id = Column(String, index=True)
    booking_time = Column(String, index=True)
    time_slot = Column(String, index=True)
    appointment_date = Column(String, index=True)
    file_data = Column(String, index=True)

    @validator("mobile_number")
    def phone_validation(cls, v):
        """Function for phone number validation"""
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{11}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number is not valid.")
        return v

class AppointmentStatus(Base):
    """Class for creating appointment status model"""
    __tablename__ = 'appointment_status'

    a_id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    