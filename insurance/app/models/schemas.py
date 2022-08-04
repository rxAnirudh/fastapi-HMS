"""Schema file for hospital table"""
from asyncio.log import logger
import re
from typing import Optional
from pydantic import BaseModel, FilePath, validator,EmailStr
from datetime import datetime


class InsuranceBase(BaseModel):
    """Base class model for insurance"""
    patient_id: Optional[str] = None
    policy_no: Optional[str] = None
    publish_date: Optional[str] = str(datetime.utcnow())
    expire_date: Optional[str] = None
    maternity: Optional[str] = None
    dental: Optional[str] = None
    optical: Optional[str] = None
    chronic_pec: Optional[str] = None
    ins_company: Optional[str] = None
    ins_plan: Optional[str] = None
    entry_fees: Optional[str] = None
    co_pay: Optional[str] = None
    co_insurance: Optional[str] = None
    med_coverage: Optional[str] = None
    
class AddNewInsurance(InsuranceBase):
    """Create class model for adding new insurance for particular patient"""
    id : int
    patient_id: Optional[str] = None
    policy_no: Optional[str] = None
    publish_date: Optional[str] = str(datetime.utcnow())
    expire_date: Optional[str] = None
    maternity: Optional[str] = None
    dental: Optional[str] = None
    optical: Optional[str] = None
    chronic_pec: Optional[str] = None
    ins_company: Optional[str] = None
    ins_plan: Optional[str] = None
    entry_fees: Optional[str] = None
    co_pay: Optional[str] = None
    co_insurance: Optional[str] = None
    med_coverage: Optional[str] = None

class AddInsuranceResponse(BaseModel):
    """Create class model for response of new insurance details to be added"""
    data : AddNewInsurance
    success : bool
    message : str

class GetInsuranceDetailsResponse(BaseModel):
    """Create class model for response of specific insurance details"""
    data : AddNewInsurance
    success : bool
    message : str


class InsuranceId(BaseModel):
    """Create class model for requesting id param in get insurance details api"""
    id : Optional[int] = None
