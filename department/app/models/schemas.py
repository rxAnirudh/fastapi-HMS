"""Schema file for department table"""
from typing import Optional 
from pydantic import BaseModel


class DepartmentBase(BaseModel): 
  """Base class model for department"""
  name: Optional[str] = None 
  head_id: Optional[str] = None 


class AddNewDepartment(DepartmentBase): 
  """Create class model for department"""
  name: Optional[str] = None 
  head_id: Optional[str] = None 
  id : int


class Response(BaseModel):
  """Create class model for response"""
  data : AddNewDepartment
  success : bool
  message : str


class DepartmentId(BaseModel):
  """Create class model for requesting id param in get department api"""
  id : Optional[int] = None