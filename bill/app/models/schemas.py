"""Schema file for patient table"""
from asyncio.log import logger
import re
from typing import Optional
from pydantic import BaseModel, FilePath, validator,EmailStr
from datetime import datetime

from sqlalchemy import TIMESTAMP

from sqlalchemy.sql import func

class BillBase(BaseModel):
    """Base class model for bill"""
    patient_id: Optional[str] = None
    doctor_charge: Optional[str] = None
    medicine_charge: Optional[str] = None
    room_charge: Optional[str] = None
    operation_charge: Optional[str] = None
    no_of_days: Optional[str] = None
    nursing_charge: Optional[str] = None
    lab_charge: Optional[str] = None
    insurance_number: Optional[str] = None
    total_bill: Optional[str] = None
    bill_date: Optional[str] = str(datetime.utcnow())
    hospital_id: Optional[str] = None
    
class AddNewBill(BillBase):
    """Create class model for bill"""
    id : int
    patient_id: Optional[str] = None
    doctor_charge: Optional[str] = None
    medicine_charge: Optional[str] = None
    room_charge: Optional[str] = None
    operation_charge: Optional[str] = None
    no_of_days: Optional[str] = None
    nursing_charge: Optional[str] = None
    lab_charge: Optional[str] = None
    insurance_number: Optional[str] = None
    total_bill: Optional[str] = None
    bill_date: Optional[str] = None
    hospital_id: Optional[str] = None

class AddBillResponse(BaseModel):
    """Create class model for response of new bill to be added"""
    data : AddNewBill
    success : bool
    message : str

class GetBillDetailsResponse(BaseModel):
    """Create class model for response of specific bill details"""
    data : AddNewBill
    success : bool
    message : str


class BillId(BaseModel):
    """Create class model for requesting id param in get bill api"""
    id : Optional[int] = None