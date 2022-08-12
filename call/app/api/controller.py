"""Controller file for writing db queries for call table"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from fastapi import HTTPException
from response import Response as ResponseData
from models import models,schemas


def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_call(database: Session, call: schemas.CallBase):
    """Function to return query based data while new call creation api"""
    db_call = models.Call(**call.__dict__)
    database.add(db_call)
    database.commit()
    database.refresh(db_call)
    return ResponseData.success(db_call.__dict__,'New Call added successfully')


def get_call_by_id(database: Session, id : Optional[int] = None):
    """Function to get call details by id"""
    db_call = database.query(models.Call).filter(models.Call.id == id).first()
    if db_call is None:
        return ResponseData.success([],'Call id is invalid')
    db_call_details = database.query(models.Call).filter(models.Call.id == id).first()
    return ResponseData.success(db_call_details.__dict__,'Call details fetched successfully')


def delete_call_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all call details if needed"""
    db_call = database.query(models.Call).filter(models.Call.id == id).first()
    if id is None:
        database.query(models.Call).delete()
        database.commit()
        return ResponseData.success([],'All Call details deleted successfully')
    database.query(models.Call).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],'Call details deleted successfully')


def update_call_details(database: Session, call: schemas.AddNewCall):
    """Function to update call details"""
    data = database.query(models.Call).filter(models.Call.id == call.id).all()
    dict1 = data[0]
    if call.dict()["staff_id"] is not None :
        dict1.__dict__["staff_id"] = call.dict()["staff_id"]
    if call.dict()["block_floor_id"] is not None :
        dict1.__dict__["block_floor_id"] = call.dict()["block_floor_id"]
    if call.dict()["block_code_id"] is not None :
        dict1.__dict__["block_code_id"] = call.dict()["block_code_id"]
    if call.dict()["on_call_start"] is not None :
        dict1.__dict__["on_call_start"] = call.dict()["on_call_start"]
    if call.dict()["on_call_end"] is not None :
        dict1.__dict__["on_call_end"] = call.dict()["on_call_end"]
    database.query(models.Call).filter(models.Call.id == call.id).update(
    {
        models.Call.id : call.id,
        models.Call.staff_id : call.staff_id,
        models.Call.block_floor_id : call.block_floor_id,
        models.Call.block_code_id : call.block_code_id,
        models.Call.on_call_start : call.on_call_start,
        models.Call.on_call_end : call.on_call_end,
    })
    database.flush()
    database.commit()
    return ResponseData.success([],'Call details Updated successfully')
