"""Schema file for hospital table"""


import re
from typing import Optional
from pydantic import BaseModel, validator,EmailStr


class HospitalBase(BaseModel):
    """Base class model for hospital"""
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None 
    country: Optional[str] = None
    hospital_type: Optional[str] = None
    is_rented: Optional[str] = None
    contact_number: Optional[str] = None


    @validator("contact_number")
    def phone_validation(cls, v):
        """Function for phone number validation"""
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{11}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number is not valid.")
        return v

    email: Optional[EmailStr] = None
    
class HospitalCreate(HospitalBase):
    """Create class model for hospital"""
    id : int
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    hospital_type: Optional[str] = None
    is_rented: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[EmailStr] = None

class CreateHospitalResponse(BaseModel):
    """Create class model for response of creating new hospital"""
    data : HospitalCreate
    success : bool
    message : str

class GetHospitalResponse(BaseModel):
    """Create class model for response of creating new hospital"""
    data : HospitalCreate
    success : bool
    message : str


class HospitalId(BaseModel):
    """Create class model for requesting id param in get hospital api"""
    id : Optional[int] = None


class HospitalName(BaseModel):
    """Create class model for requesting hospital name param in get hospital api"""
    name : Optional[str] = None