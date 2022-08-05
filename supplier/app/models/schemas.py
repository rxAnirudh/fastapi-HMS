"""Schema file for hospital table"""


from typing import Optional
from pydantic import BaseModel


class SupplierBase(BaseModel):
    """Base class model for supplier"""
    company: Optional[str] = None
    contact_number: Optional[str] = None
    email_id: Optional[str] = None
    address: Optional[str] = None


class AddNewSupplier(SupplierBase):
    """Create class model for supplier"""
    id : int
    company: Optional[str] = None
    contact_number: Optional[str] = None
    email_id: Optional[str] = None
    address: Optional[str] = None


class AddSupplierResponse(BaseModel):
    """Create class model for response of new supplier to be added"""
    data : AddNewSupplier
    success : bool
    message : str

class GetSupplierDetailsResponse(BaseModel):
    """Create class model for response of specific supplier details"""
    data : AddNewSupplier
    success : bool
    message : str


class SupplierId(BaseModel):
    """Create class model for requesting id param in get supplier api"""
    id : Optional[int] = None
