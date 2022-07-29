"""File for hospital route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import schemas
from db import get_db
from typing import List

from api import controller

hospital_router = APIRouter()


@hospital_router.post("/create_hospital", response_model=schemas.CreateHospitalResponse)
def create_hospital(hospital: schemas.HospitalBase, database: Session = Depends(get_db)):
    """Function to return final response while creating new_hospital creation api"""
    db_hospital = controller.get_hospital(database, contact_number=hospital.contact_number)
    if db_hospital:
        raise HTTPException(status_code=400, detail="Hospital already registered with same contact number")
    return controller.create_hospital(database,hospital)


@hospital_router.post("/get_hospital")
def get_hospital(hospitalid: schemas.HospitalId, database: Session = Depends(get_db)):
    """Function to return hospital details
    (specific and all hospitals data can be fetched)"""
    return controller.get_hospital_by_id(database, id = hospitalid.id)


@hospital_router.post("/delete_hospital")
def delete_hospital(hospitalid: schemas.HospitalId, database: Session = Depends(get_db)):
    """Function to return hospital details
    (specific and all hospitals data can be fetched)"""
    return controller.delete_hospital(database, id = hospitalid.id)


@hospital_router.post("/update_hospital")
def update_hospital(hospital_details: schemas.HospitalCreate, database: Session = Depends(get_db)):
    """Function to update particular hospital details"""
    return controller.update_hospital(database, hospital = hospital_details)
