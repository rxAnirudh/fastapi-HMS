"""Schema file for call table"""
from typing import Optional 
from pydantic import BaseModel


class CallBase(BaseModel): 
  """Base class model for call"""
  staff_id: Optional[str] = None 
  block_floor_id: Optional[str] = None 
  block_code_id: Optional[str] = None 
  on_call_start: Optional[str] = None 
  on_call_end: Optional[str] = None 


class AddNewCall(CallBase): 
  """Create class model for call"""
  staff_id: Optional[str] = None 
  block_floor_id: Optional[str] = None 
  block_code_id: Optional[str] = None 
  on_call_start: Optional[str] = None 
  on_call_end: Optional[str] = None 
  id : int


class Response(BaseModel):
  """Create class model for response"""
  data : AddNewCall
  success : bool
  message : str


class CallId(BaseModel):
  """Create class model for requesting id param in get call api"""
  id : Optional[int] = None