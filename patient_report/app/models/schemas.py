"""Schema file for hospital table"""
from asyncio.log import logger
import re
from typing import Optional
from pydantic import BaseModel, FilePath, validator,EmailStr


class PatientReportBase(BaseModel):
    """Base class model for patient report"""
    patient_id: Optional[str] = None
    report_id: Optional[str] = None
    diagnose: Optional[str] = None
    reference: Optional[str] = None
    medicine_id: Optional[str] = None
    medicine_name: Optional[str] = None
    doctor_id: Optional[str] = None
    hospital_id: Optional[str] = None
    
class AddNewPatientReport(PatientReportBase):
    """Create class model for patient report"""
    id : int
    patient_id: Optional[str] = None
    report_id: Optional[str] = None
    diagnose: Optional[str] = None
    reference: Optional[str] = None
    medicine_id: Optional[str] = None
    medicine_name: Optional[str] = None
    doctor_id: Optional[str] = None
    hospital_id: Optional[str] = None

class AddPatientReportResponse(BaseModel):
    """Create class model for response of new patient report to be added"""
    data : AddNewPatientReport
    success : bool
    message : str

class GetSupplierDetailsResponse(BaseModel):
    """Create class model for response of specific patient report details"""
    data : AddNewPatientReport
    success : bool
    message : str


class PatientReportId(BaseModel):
    """Create class model for requesting id param in get patient report api"""
    id : Optional[int] = None
