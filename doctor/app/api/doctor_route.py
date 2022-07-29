"""File for hospital route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import schemas
from db import get_db
from typing import List

from api import controller

doctor_router = APIRouter()


@doctor_router.post("/add_doctor", response_model=schemas.AddDoctorResponse)
def add_doctor(doctor: schemas.DoctorBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new doctor details"""
    db_doctor = controller.get_doctor(database, contact_number=doctor.contact_number)
    if db_doctor:
        raise HTTPException(status_code=400, detail="Doctor already registered with same contact number")
    return controller.add_new_doctor(database,doctor)


@doctor_router.post("/get_doctor_details")
def get_doctor(doctodid: schemas.DoctorId, database: Session = Depends(get_db)):
    """Function to return doctor details
    (specific and all doctor data can be fetched)"""
    return controller.get_doctor_by_id(database, id = doctodid.id)


@doctor_router.post("/delete_doctor_details")
def delete_doctor(doctodid: schemas.DoctorId, database: Session = Depends(get_db)):
    """Function to return doctor details
    (specific and all hospitals data can be fetched)"""
    return controller.delete_doctor_details(database, id = doctodid.id)


@doctor_router.post("/update_doctor_details")
def update_doctor_details(doctor_details: schemas.AddNewDoctor, database: Session = Depends(get_db)):
    """Function to update particular doctor details"""
    return controller.update_doctor_details(database, doctor = doctor_details)
