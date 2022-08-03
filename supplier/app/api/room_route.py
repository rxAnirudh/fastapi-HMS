"""File for hospital route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import schemas
from db import get_db

from api import controller

room_router = APIRouter()


@room_router.post("/add_new_room", response_model=schemas.AddRoomResponse)
def add_new_room(room: schemas.RoomBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new room details"""
    return controller.add_new_room(database,room)


@room_router.post("/get_room_details")
def get_room_details(roomid: schemas.RoomId, database: Session = Depends(get_db)):
    """Function to return Room details
    (specific and all Room data can be fetched)"""
    return controller.get_room_by_id(database, id = roomid.id)


@room_router.post("/delete_room_details")
def delete_room_details(roomid: schemas.RoomId, database: Session = Depends(get_db)):
    """Function to return Room details
    (specific and all Room data can be fetched)"""
    return controller.delete_room_details(database, id = roomid.id)


@room_router.post("/update_room_details")
def update_room_details(room_details: schemas.AddNewRoom, database: Session = Depends(get_db)):
    """Function to update particular Room details"""
    return controller.update_room_details(database, room = room_details)


@room_router.post("/add_room_status", response_model=schemas.AddRoomStatusResponse)
def add_room_status(room_status: schemas.RoomStatusBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new Room status details"""
    return controller.add_room_status(database,room_status)


@room_router.post("/get_room_status")
def get_room_status(room_status_id: schemas.RoomStatusId, database: Session = Depends(get_db)):
    """Function to return Room details
    (specific and all Room status data can be fetched)"""
    return controller.get_room_status_by_id_or_without_id(database, id = room_status_id.id)


@room_router.post("/delete_room_status")
def delete_room_status(room_status_id: schemas.RoomStatusId, database: Session = Depends(get_db)):
    """Function to return Room details
    (specific and all Room data can be fetched)"""
    return controller.delete_room_status(database, id = room_status_id.id)


@room_router.post("/update_room_status")
def update_room_status(room_status: schemas.AddNewRoomStatus, database: Session = Depends(get_db)):
    """Function to update particular Room status details"""
    return controller.update_room_status_details(database, room_status = room_status)