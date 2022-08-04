"""Schema file for patient table"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FeedbackBase(BaseModel):
    """Base class model for feedback"""
    from_patient_id: Optional[str] = None
    to_staff_id: Optional[str] = None
    comment: Optional[str] = None
    rating: Optional[str] = None
    created_on: Optional[str] = str(datetime.utcnow())
    updated_on: Optional[str] = str(datetime.utcnow())
    hospital_id : Optional[str] = None
    
class AddNewFeedback(FeedbackBase):
    """Create class model for feedback"""
    id : int
    from_patient_id: Optional[str] = None
    to_staff_id: Optional[str] = None
    comment: Optional[str] = None
    rating: Optional[str] = None
    created_on: Optional[str] = str(datetime.utcnow())
    updated_on: Optional[str] = str(datetime.utcnow())
    hospital_id : Optional[str] = None

class AddFeedbackResponse(BaseModel):
    """Create class model for response of new feedback to be added"""
    data : AddNewFeedback
    success : bool
    message : str

class GetFeedbackDetailsResponse(BaseModel):
    """Create class model for response of specific feedback details"""
    data : AddNewFeedback
    success : bool
    message : str


class FeedbackId(BaseModel):
    """Create class model for requesting id param in get feedback api"""
    id : Optional[int] = None