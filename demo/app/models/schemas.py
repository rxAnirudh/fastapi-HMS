"""Schema file for demo table"""
from typing import Optional 
from pydantic import BaseModel


class DemoBase(BaseModel): 
  """Base class model for demo"""
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


class AddNewDemo(DemoBase): 
  """Create class model for demo"""
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
  id : int


class Response(BaseModel):
  """Create class model for response"""
  data : AddNewDemo
  success : bool
  message : str


class DemoId(BaseModel):
  """Create class model for requesting id param in get demo api"""
  id : Optional[int] = None