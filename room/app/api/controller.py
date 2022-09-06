import sys
import os
from fastapi import HTTPException
sys.path.append(os.getcwd())
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_room(database: Session, room: schemas.RoomBase):
    """Function to return query based data while creating new room creation api"""
    if not check_if_hospital_id_is_valid(database,room.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    is_status_id_valid = database.query(models.RoomStatus).filter(models.RoomStatus.id == room.dict()["status"]).first()
    if not is_status_id_valid:
        raise HTTPException(status_code=400, detail="status id is invalid")
    db_room = models.Room(**room.__dict__)
    database.add(db_room)
    database.commit()
    database.refresh(db_room)
    return ResponseData.success(db_room.__dict__,"New Room added successfully")

def get_room_by_id(database: Session, id : Optional[int] = None):
    """Function to get room details based on room id generated while adding new room"""
    db_room = database.query(models.Room).filter(models.Room.id == id).first()
    if db_room is None:
        return ResponseData.success([],"Room id is invalid")
    db_room_details = database.query(models.Room).filter(models.Room.id == id).first()
    return ResponseData.success(db_room_details.__dict__,"Room details fetched successfully")

def delete_room_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all room details if needed"""
    if id is None:
        database.query(models.Room).delete()
        database.commit()
        return ResponseData.success([],"All Room details deleted successfully")
    database.query(models.Room).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Room details deleted successfully")

def update_room_details(database: Session, room: schemas.AddNewRoom):
    """Function to update room details"""
    data = database.query(models.Room).filter(models.Room.id == room.id).all()
    dict1 = data[0]
    if room.dict()["type"] is not None :
        dict1.__dict__["type"] = room.dict()["type"]
    if room.dict()["status"] is not None :
        dict1.__dict__["status"] = room.dict()["status"]
    if room.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = room.dict()["hospital_id"]
    database.query(models.Room).filter(models.Room.id == room.id).update({ models.Room.id : room.id,
        models.Room.type: dict1.__dict__["type"],
        models.Room.hospital_id : dict1.__dict__["hospital_id"],
        models.Room.status : dict1.__dict__["status"]
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Room details updated successfully")


def add_room_status(database: Session, room_status: schemas.RoomStatusBase):
    """Function to return query based data while creating new room status creation api"""
    room_status_dict = {'status': room_status.dict()["status"]}
    db_room_status = models.RoomStatus(**room_status_dict)
    database.add(db_room_status)
    database.commit()
    database.refresh(db_room_status)
    db_room_status.__dict__["id"] = db_room_status.id
    return ResponseData.success(db_room_status.__dict__,"Room status added successfully")

def get_room_status_by_id_or_without_id(database: Session, id : Optional[int] = None):
    """Function to get room status details"""
    if id is None:
        db_room_status_details = database.query(models.RoomStatus).filter().all()
        return ResponseData.success(db_room_status_details.__dict__,"Room status details fetched successfully")
    db_room_status = database.query(models.RoomStatus).filter(models.RoomStatus.id == id).first()
    if db_room_status is None:
        return ResponseData.success([],"Room status id is invalid")
    db_room_status_details = database.query(models.RoomStatus).filter(models.RoomStatus.id == id).first()
    return ResponseData.success(db_room_status_details.__dict__,"Room status details fetched successfully")

def delete_room_status(database: Session, id : Optional[int] = None):
    """Function to delete single or all room status if needed"""
    if id is None:
        database.query(models.RoomStatus).delete()
        database.commit()
        return ResponseData.success([],"All Room status deleted successfully")
    database.query(models.RoomStatus).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Room status deleted successfully")

def update_room_status_details(database: Session, room_status: schemas.AddNewRoomStatus):
    """Function to update room status details"""
    data = database.query(models.RoomStatus).filter(models.RoomStatus.id == room_status.id).all()
    dict1 = data[0]["RoomStatus"]
    if room_status.dict()["status"] is not None :
        dict1.__dict__["status"] = room_status.dict()["status"]
    database.query(models.RoomStatus).filter(models.RoomStatus.id == room_status.id).update({ models.RoomStatus.id : room_status.id,
        models.RoomStatus.status: dict1.__dict__["status"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Room status details updated successfully")