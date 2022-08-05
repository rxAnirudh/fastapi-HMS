"""Schema file for hospital table"""


from typing import Optional
from pydantic import BaseModel


class AppointmentBase(BaseModel):
    """Base class model for appointment"""
    patient_id: Optional[str] = None
    hospital_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status_id: Optional[str] = None
    booking_time: Optional[str] = None

class AppointmentStatusBase(BaseModel):
    """Base class model for appointment"""
    status: Optional[str] = None
    
class AddNewAppointment(AppointmentBase):
    """Create class model for appointment"""
    id : int
    patient_id: Optional[str] = None
    hospital_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status_id: Optional[str] = None
    booking_time: Optional[str] = None

class AddNewAppointmentStatus(AppointmentStatusBase):
    """Create class model for appointment status"""
    a_id : int
    status: Optional[str] = None

class AddAppointmentResponse(BaseModel):
    """Create class model for response of new appointment to be added"""
    data : AddNewAppointment
    success : bool
    message : str

class AddAppointmentStatusResponse(BaseModel):
    """Create class model for response of new appointment status to be added"""
    data : AddNewAppointmentStatus
    success : bool
    message : str

class GetAppointmentDetailsResponse(BaseModel):
    """Create class model for response of specific appointment details"""
    data : AddNewAppointment
    success : bool
    message : str


class AppointmentId(BaseModel):
    """Create class model for requesting id param in get appointment api"""
    id : Optional[int] = None

class AppointmentStatusId(BaseModel):
    """Create class model for requesting id param in get appointment status api"""
    a_id : Optional[int] = None