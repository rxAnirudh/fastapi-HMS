"""Schema file for hospital table"""


import re
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class DoctorBase(BaseModel):
    """Base class model for doctor"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_number: Optional[str] = None
    profile_pic: Optional[str] = None
    email: Optional[str] = None
    blood_group: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    years_of_experience: Optional[str] = None
    next_available_at: Optional[str] = None
    specialist_field: Optional[str] = None
    education: Optional[str] = None
    in_clinic_appointment_fees: Optional[str] = None
    create_at: Optional[str] = None
    # patients_comment: Optional[str] = None
    @validator("contact_number")
    def phone_validation(cls, v):
        """Function for phone number validation"""
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{11}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number is not valid.")
        return v
    email: Optional[EmailStr] = None
    
class AddNewDoctor(DoctorBase):
    """Create class model for doctor"""
    id : int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_number: Optional[str] = None
    profile_pic: Optional[str] = None
    email: Optional[str] = None
    blood_group: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    years_of_experience: Optional[str] = None
    next_available_at: Optional[str] = None
    specialist_field: Optional[str] = None
    education: Optional[str] = None
    in_clinic_appointment_fees: Optional[str] = None
    create_at: Optional[str] = None
    # patients_comment: Optional[str] = None

class AddDoctorResponse(BaseModel):
    """Create class model for response of new doctor to be added"""
    data : AddNewDoctor
    success : bool
    message : str

class GetDoctorDetailsResponse(BaseModel):
    """Create class model for response of specific doctor details"""
    data : AddNewDoctor
    success : bool
    message : str


class DoctorId(BaseModel):
    """Create class model for requesting id param in get doctor api"""
    id : Optional[int] = None