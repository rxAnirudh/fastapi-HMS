"""Schema file for patient table"""
from asyncio.log import logger
import re
from typing import Optional
from pydantic import BaseModel, FilePath, validator,EmailStr


class PatientBase(BaseModel):
    """Base class model for patient"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_number: Optional[str] = None
    profile_pic: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    city: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    past_injuries: Optional[str] = None
    past_surgeries: Optional[str] = None
    smoking_habits: Optional[str] = None
    alchol_consumption: Optional[str] = None
    activity_level: Optional[str] = None
    food_preference: Optional[str] = None
    occupation: Optional[str] = None
    hospital_id: Optional[str] = None
    
    @validator("contact_number")
    def phone_validation(cls, v):
        """Function for phone number validation"""
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{11}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number is not valid.")
        return v
    email: Optional[EmailStr] = None
    
class AddNewPatient(PatientBase):
    """Create class model for patient"""
    id : int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_number: Optional[str] = None
    profile_pic: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    city: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    past_injuries: Optional[str] = None
    past_surgeries: Optional[str] = None
    smoking_habits: Optional[str] = None
    alchol_consumption: Optional[str] = None
    activity_level: Optional[str] = None
    food_preference: Optional[str] = None
    occupation: Optional[str] = None
    hospital_id: Optional[str] = None

class AddPatientResponse(BaseModel):
    """Create class model for response of new patient to be added"""
    data : AddNewPatient
    success : bool
    message : str

class GetPatientDetailsResponse(BaseModel):
    """Create class model for response of specific patient details"""
    data : AddNewPatient
    success : bool
    message : str


class PatientId(BaseModel):
    """Create class model for requesting id param in get patient api"""
    id : Optional[int] = None