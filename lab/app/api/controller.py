import sys

from fastapi import HTTPException
from datetime import datetime
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.api.controller import check_if_patient_id_is_valid
from staff.app.api.controller import check_if_staff_id_is_valid




# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_lab(database: Session, lab: schemas.LabBase):
    """Function to return query based data while creating new lab creation api"""
    if not check_if_hospital_id_is_valid(database,lab.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_patient_id_is_valid(database,lab.dict()["patient_id"]):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    if not check_if_staff_id_is_valid(database,lab.dict()["patient_id"]):
        raise HTTPException(status_code=400, detail="Staff id is invalid")
    db_lab = models.Lab(**lab.__dict__)
    database.add(db_lab)
    database.commit()
    database.refresh(db_lab)
    return ResponseData.success(db_lab.__dict__,"Lab added successfully")

def get_lab_by_id(database: Session, id : Optional[int] = None):
    """Function to get lab details by id"""
    db_lab = database.query(models.Lab).filter(models.Lab.id == id).first()
    if db_lab is None:
        return ResponseData.success([],"Lab with this id does not exists")
    return ResponseData.success(db_lab.__dict__,"Lab details fetched successfully")

def delete_lab_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all lab details if needed"""
    if id is None:
        database.query(models.Lab).delete()
        database.commit()
        return ResponseData.success([],"All Lab details deleted successfully")
    db_lab = database.query(models.Lab).filter(id == id).first()
    if db_lab is None:
        return ResponseData.success([],"Lab with this id does not exists")
    database.query(models.Lab).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Lab details deleted successfully")

def update_lab_details(database: Session, lab: schemas.AddNewLab):
    """Function to update lab details"""
    data = database.query(models.Lab).filter(models.Lab.id == lab.id).all()
    dict1 = data[0]
    if lab.dict()["staff_id"] is not None :
        dict1.__dict__["staff_id"] = lab.dict()["staff_id"]
    if lab.dict()["patient_id"] is not None :
        dict1.__dict__["patient_id"] = lab.dict()["patient_id"]
    if lab.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = lab.dict()["hospital_id"]
    if lab.dict()["test_type"] is not None :
        dict1.__dict__["test_type"] = lab.dict()["test_type"]
    if lab.dict()["test_code"] is not None :
        dict1.__dict__["test_code"] = lab.dict()["test_code"]
    if lab.dict()["weight"] is not None :
        dict1.__dict__["weight"] = lab.dict()["weight"]
    if lab.dict()["height"] is not None :
        dict1.__dict__["height"] = lab.dict()["height"]
    if lab.dict()["blood_pressure"] is not None :
        dict1.__dict__["blood_pressure"] = lab.dict()["blood_pressure"]
    if lab.dict()["test_result"] is not None :
        dict1.__dict__["test_result"] = lab.dict()["test_result"]
    if lab.dict()["updated_at"] is not None :
        dict1.__dict__["updated_at"] = lab.dict()["updated_at"]
    if lab.dict()["updated_at"] is None :
        dict1.__dict__["updated_at"] = str(datetime.now())
    database.query(models.Lab).filter(models.Lab.id == lab.id).update({ models.Lab.id : lab.id,
        models.Lab.patient_id: dict1.__dict__["patient_id"],
        models.Lab.staff_id : dict1.__dict__["staff_id"],
        models.Lab.hospital_id : dict1.__dict__["hospital_id"],
        models.Lab.test_type : dict1.__dict__["test_type"],
        models.Lab.test_code : dict1.__dict__["test_code"],
        models.Lab.weight : dict1.__dict__["weight"],
        models.Lab.height : dict1.__dict__["height"],
        models.Lab.blood_pressure : dict1.__dict__["blood_pressure"],
        models.Lab.test_result : dict1.__dict__["test_result"],
        models.Lab.updated_at : dict1.__dict__["updated_at"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Lab details updated successfully")
