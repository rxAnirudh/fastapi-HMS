"""File for creating models of the project"""

from sqlalchemy import Column, TIMESTAMP, Integer,  String,Boolean
from db import Base

class Room(Base):
    """Class for creating room model"""
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    status = Column(String, index=True)
    hospital_id = Column(String, index=True)

class RoomStatus(Base):
    """Class for creating room status model"""
    __tablename__ = 'room_status'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    