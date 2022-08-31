"""Schema file for patient table"""


import re
from typing import Optional
from fastapi import File
from pydantic import BaseModel, EmailStr, NonNegativeInt, validator,SecretStr


class PatientBase(BaseModel):
    """Base class model for patient"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_number: Optional[str] = None
    password: Optional[str] = None
    profile_pic: Optional[bytes] = File(None)
    email: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    city: Optional[str] = None
    allergy: Optional[str] = None
    current_medication: Optional[str] = None
    past_injury: Optional[str] = None
    past_surgery: Optional[str] = None
    smoking_habits: Optional[str] = None
    alchol_consumption: Optional[str] = None
    activity_level: Optional[str] = None
    food_preference: Optional[str] = None
    occupation: Optional[str] = None
    hospital_id: Optional[NonNegativeInt] = None
    
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
    password: Optional[str] = None
    profile_pic: Optional[bytes] = File(None)
    email: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    city: Optional[str] = None
    allergy: Optional[str] = None
    current_medication: Optional[str] = None
    past_injury: Optional[str] = None
    past_surgery: Optional[str] = None
    smoking_habits: Optional[str] = None
    alchol_consumption: Optional[str] = None
    activity_level: Optional[str] = None
    food_preference: Optional[str] = None
    occupation: Optional[str] = None
    hospital_id: Optional[NonNegativeInt] = None
    # authentication_token: Optional[map] = None

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

class PatientEmail(BaseModel):
    """Create class model for requesting id param in get patient api"""
    email : Optional[str] = None
    password : Optional[str] = None

class PatientPassword(BaseModel):
    """Create class model for requesting id param in get patient api"""
    password : Optional[str] = None

class AllergyId(BaseModel):
    """Create class model for requesting id param in get patient allergies api"""
    id : Optional[int] = None
    allergy_name : Optional[str] = None

class FoodPreferenceId(BaseModel):
    """Create class model for requesting id param in get food preference api"""
    id : Optional[int] = None
    food_preference_name : Optional[str] = None

class CurrentMedicationId(BaseModel):
    """Create class model for requesting id param in get patient current medications api"""
    id : Optional[int] = None
    current_medication_name : Optional[str] = None

class PastInjuries(BaseModel):
    """Create class model for requesting id param in get patient past injuries api"""
    id : Optional[int] = None
    past_injury : Optional[str] = None

class PastSurgeries(BaseModel):
    """Create class model for requesting id param in get patient past surgeries api"""
    id : Optional[int] = None
    past_surgery : Optional[str] = None