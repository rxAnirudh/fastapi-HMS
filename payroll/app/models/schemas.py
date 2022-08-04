"""Schema file for patient table"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PayrollBase(BaseModel):
    """Base class model for payroll"""
    staff_id: Optional[str] = None
    salary: Optional[str] = None
    net_salary: Optional[str] = None
    hourly_salary: Optional[str] = None
    bonus_salary: Optional[str] = None
    compensation: Optional[str] = None
    account_no: Optional[str] = None
    hospital_id: Optional[str] = None
    
    
class AddNewPayroll(PayrollBase):
    """Create class model for payroll"""
    id : int
    staff_id: Optional[str] = None
    salary: Optional[str] = None
    net_salary: Optional[str] = None
    hourly_salary: Optional[str] = None
    bonus_salary: Optional[str] = None
    compensation: Optional[str] = None
    account_no: Optional[str] = None
    hospital_id: Optional[str] = None

class AddPayrollResponse(BaseModel):
    """Create class model for response of new payroll to be added"""
    data : AddNewPayroll
    success : bool
    message : str

class GetPayrollDetailsResponse(BaseModel):
    """Create class model for response of specific payroll details"""
    data : AddNewPayroll
    success : bool
    message : str


class PayrollId(BaseModel):
    """Create class model for requesting id param in get payroll api"""
    id : Optional[int] = None