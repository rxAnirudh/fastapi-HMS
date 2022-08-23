"""Schema file for affiliation table"""
from typing import Optional 
from pydantic import BaseModel


class AffiliationBase(BaseModel): 
  """Base class model for affiliation"""
  staff_id: Optional[str] = None 
  department_id: Optional[str] = None 
  primaryaffiliation: Optional[str] = None 


class AddNewAffiliation(AffiliationBase): 
  """Create class model for affiliation"""
  staff_id: Optional[str] = None 
  department_id: Optional[str] = None 
  primaryaffiliation: Optional[str] = None 
  id : int


class Response(BaseModel):
  """Create class model for response"""
  data : AddNewAffiliation
  success : bool
  message : str


class AffiliationId(BaseModel):
  """Create class model for requesting id param in get affiliation api"""
  id : Optional[int] = None