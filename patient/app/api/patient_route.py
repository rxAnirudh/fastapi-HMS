"""File for patient route"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from patient.app.models import schemas
from db import get_db

from api import controller

patient_router = APIRouter()


@patient_router.post("/add_patient", response_model=schemas.AddPatientResponse)
def add_patient(patient: schemas.PatientBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new patient details"""
    db_patient = controller.get_patient(database, contact_number=patient.contact_number)
    if db_patient:
        raise HTTPException(status_code=400, detail="Patient already registered with same contact number")
    return controller.add_new_patient(database,patient)


@patient_router.post("/get_patient_details")
def get_patient(patientid: schemas.PatientId, database: Session = Depends(get_db)):
    """Function to return patient details
    (specific and all patient data can be fetched)"""
    return controller.get_patient_by_id(database, id = patientid.id)


@patient_router.post("/delete_patient_details")
def delete_patient(patientid: schemas.PatientId, database: Session = Depends(get_db)):
    """Function to return patient details
    (specific and all patient data can be fetched)"""
    return controller.delete_patient_details(database, id = patientid.id)


@patient_router.post("/update_patient_details")
def update_patient_details(patient_details: schemas.AddNewPatient, database: Session = Depends(get_db)):
    """Function to update particular patient details"""
    return controller.update_patient_details(database, patient = patient_details)
