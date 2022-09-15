"""Schema file for hospital table"""


import re
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class StaffBase(BaseModel):
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
    education: Optional[str] = None
    create_at: Optional[str] = None
    hospital_id : Optional[int] = None
    # patients_comment: Optional[str] = None
    @validator("contact_number")
    def phone_validation(cls, v):
        """Function for phone number validation"""
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{11}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number is not valid.")
        return v
    email: Optional[EmailStr] = None
    
class AddNewStaff(StaffBase):
    """Create class model for staff"""
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
    education: Optional[str] = None
    create_at: Optional[str] = None
    hospital_id : Optional[int] = None
    # patients_comment: Optional[str] = None

class AddStaffResponse(BaseModel):
    """Create class model for response of new staff to be added"""
    data : AddNewStaff
    success : bool
    message : str

class GetStaffDetailsResponse(BaseModel):
    """Create class model for response of specific staff details"""
    data : AddNewStaff
    success : bool
    message : str


class StaffId(BaseModel):
    """Create class model for requesting id param in get staff api"""
    id : Optional[int] = None