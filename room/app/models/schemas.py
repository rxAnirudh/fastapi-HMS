"""Schema file for hospital table"""
from asyncio.log import logger
import re
from typing import Optional
from pydantic import BaseModel, FilePath, validator,EmailStr


class RoomBase(BaseModel):
    """Base class model for room"""
    type: Optional[str] = None
    status: Optional[str] = None
    hospital_id: Optional[str] = None

class RoomStatusBase(BaseModel):
    """Base class model for room"""
    status: Optional[str] = None
    
class AddNewRoom(RoomBase):
    """Create class model for room"""
    id : int
    type: Optional[str] = None
    status: Optional[str] = None
    hospital_id: Optional[str] = None

class AddNewRoomStatus(RoomStatusBase):
    """Create class model for room status"""
    id : int
    status: Optional[str] = None

class AddRoomResponse(BaseModel):
    """Create class model for response of new room to be added"""
    data : AddNewRoom
    success : bool
    message : str

class AddRoomStatusResponse(BaseModel):
    """Create class model for response of new room status to be added"""
    data : AddNewRoomStatus
    success : bool
    message : str

class GetRoomDetailsResponse(BaseModel):
    """Create class model for response of specific room details"""
    data : AddNewRoom
    success : bool
    message : str


class RoomId(BaseModel):
    """Create class model for requesting id param in get room api"""
    id : Optional[int] = None

class RoomStatusId(BaseModel):
    """Create class model for requesting id param in get room status api"""
    id : Optional[int] = None