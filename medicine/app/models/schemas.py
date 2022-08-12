"""Schema file for patient table"""


from typing import Optional
from pydantic import BaseModel


class MedicineBase(BaseModel):
    """Base class model for medicine"""
    name: Optional[str] = None
    type: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    quantity: Optional[str] = None
    production_date: Optional[str] = None
    expire_date: Optional[str] = None
    country: Optional[str] = None
    supplier_id: Optional[str] = None
    
class AddNewMedicine(MedicineBase):
    """Create class model for medicine"""
    id : int
    name: Optional[str] = None
    type: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    quantity: Optional[str] = None
    production_date: Optional[str] = None
    expire_date: Optional[str] = None
    country: Optional[str] = None
    supplier_id: Optional[str] = None

class AddMedicineResponse(BaseModel):
    """Create class model for response of new medicine to be added"""
    data : AddNewMedicine
    success : bool
    message : str

class GetPatientDetailsResponse(BaseModel):
    """Create class model for response of specific medicine details"""
    data : AddNewMedicine
    success : bool
    message : str


class MedicineId(BaseModel):
    """Create class model for requesting id param in get medicine api"""
    id : Optional[int] = None