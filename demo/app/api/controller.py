"""Controller file for writing db queries for demo table"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from fastapi import HTTPException
from response import Response as ResponseData
from models import models,schemas


def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_demo(database: Session, demo: schemas.DemoBase):
    """Function to return query based data while new demo creation api"""
    db_demo = models.Demo(**demo.__dict__)
    database.add(db_demo)
    database.commit()
    database.refresh(db_demo)
    return ResponseData.success(db_demo.__dict__,'New Demo added successfully')


def get_demo_by_id(database: Session, id : Optional[int] = None):
    """Function to get demo details by id"""
    db_demo = database.query(models.Demo).filter(models.Demo.id == id).first()
    if db_demo is None:
        return ResponseData.success([],'Demo id is invalid')
    db_demo_details = database.query(models.Demo).filter(models.Demo.id == id).first()
    return ResponseData.success(db_demo_details.__dict__,'Demo details fetched successfully')


def delete_demo_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all demo details if needed"""
    db_demo = database.query(models.Demo).filter(models.Demo.id == id).first()
    if id is None:
        database.query(models.Demo).delete()
        database.commit()
        return ResponseData.success([],'All Demo details deleted successfully')
    database.query(models.Demo).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],'Demo details deleted successfully')


def update_demo_details(database: Session, demo: schemas.AddNewDemo):
    """Function to update demo details"""
    data = database.query(models.Demo).filter(models.Demo.id == demo.id).all()
    dict1 = data[0]
    if demo.dict()["patient_id"] is not None :
        dict1.__dict__["patient_id"] = demo.dict()["patient_id"]
    if demo.dict()["doctor_charge"] is not None :
        dict1.__dict__["doctor_charge"] = demo.dict()["doctor_charge"]
    if demo.dict()["medicine_charge"] is not None :
        dict1.__dict__["medicine_charge"] = demo.dict()["medicine_charge"]
    if demo.dict()["room_charge"] is not None :
        dict1.__dict__["room_charge"] = demo.dict()["room_charge"]
    if demo.dict()["operation_charge"] is not None :
        dict1.__dict__["operation_charge"] = demo.dict()["operation_charge"]
    if demo.dict()["no_of_days"] is not None :
        dict1.__dict__["no_of_days"] = demo.dict()["no_of_days"]
    if demo.dict()["nursing_charge"] is not None :
        dict1.__dict__["nursing_charge"] = demo.dict()["nursing_charge"]
    if demo.dict()["lab_charge"] is not None :
        dict1.__dict__["lab_charge"] = demo.dict()["lab_charge"]
    if demo.dict()["insurance_number"] is not None :
        dict1.__dict__["insurance_number"] = demo.dict()["insurance_number"]
    if demo.dict()["total_bill"] is not None :
        dict1.__dict__["total_bill"] = demo.dict()["total_bill"]
    if demo.dict()["bill_date"] is not None :
        dict1.__dict__["bill_date"] = demo.dict()["bill_date"]
    if demo.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = demo.dict()["hospital_id"]
    database.query(models.Demo).filter(models.Demo.id == demo.id).update(
    {
        models.Demo.id : demo.id,
        models.Demo.patient_id : demo.patient_id,
        models.Demo.doctor_charge : demo.doctor_charge,
        models.Demo.medicine_charge : demo.medicine_charge,
        models.Demo.room_charge : demo.room_charge,
        models.Demo.operation_charge : demo.operation_charge,
        models.Demo.no_of_days : demo.no_of_days,
        models.Demo.nursing_charge : demo.nursing_charge,
        models.Demo.lab_charge : demo.lab_charge,
        models.Demo.insurance_number : demo.insurance_number,
        models.Demo.total_bill : demo.total_bill,
        models.Demo.bill_date : demo.bill_date,
        models.Demo.hospital_id : demo.hospital_id,
    })
    database.flush()
    database.commit()
    return ResponseData.success([],'Demo details deleted successfully')
