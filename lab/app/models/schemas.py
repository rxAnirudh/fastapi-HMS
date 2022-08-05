"""Schema file for patient table"""


from typing import Optional
from pydantic import BaseModel, validator,EmailStr
from datetime import datetime

class LabBase(BaseModel):
    """Base class model for lab"""
    staff_id: Optional[str] = None
    patient_id: Optional[str] = None
    test_type: Optional[str] = None
    test_code: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    blood_pressure: Optional[str] = None
    test_result: Optional[str] = None
    created_at: Optional[str] = str(datetime.utcnow())
    updated_at: Optional[str] = str(datetime.utcnow())
    hospital_id: Optional[str] = None
    
class AddNewLab(LabBase):
    """Create class model for lab"""
    id : int
    staff_id: Optional[str] = None
    patient_id: Optional[str] = None
    test_type: Optional[str] = None
    test_code: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    blood_pressure: Optional[str] = None
    test_result: Optional[str] = None
    created_at: Optional[str] = str(datetime.utcnow())
    updated_at: Optional[str] = str(datetime.utcnow())
    hospital_id: Optional[str] = None

class AddLabResponse(BaseModel):
    """Create class model for response of new lab to be added"""
    data : AddNewLab
    success : bool
    message : str

class GetLabDetailsResponse(BaseModel):
    """Create class model for response of specific lab details"""
    data : AddNewLab
    success : bool
    message : str


class LabId(BaseModel):
    """Create class model for requesting id param in get lab api"""
    id : Optional[int] = None