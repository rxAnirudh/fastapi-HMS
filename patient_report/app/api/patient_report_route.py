"""File for hospital route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import schemas
from db import get_db

from api import controller

patient_report_router = APIRouter()


@patient_report_router.post("/add_new_patient_report", response_model=schemas.AddPatientReportResponse)
def add_new_patient_report(patient_report: schemas.PatientReportBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new patient report details"""
    return controller.add_new_patient_report(database,patient_report)


@patient_report_router.post("/get_patient_report_details")
def get_patient_report_details(patient_report_id: schemas.PatientReportId, database: Session = Depends(get_db)):
    """Function to return patient report details
    (specific and all patient report data can be fetched)"""
    return controller.get_patient_report_by_id(database, id = patient_report_id.id)


@patient_report_router.post("/delete_patient_report_details")
def delete_patient_report_details(patient_report_id: schemas.PatientReportId, database: Session = Depends(get_db)):
    """Function to return patient report details
    (specific and all patient report data can be fetched)"""
    return controller.delete_patient_report_details(database, id = patient_report_id.id)


@patient_report_router.post("/update_patient_report_details")
def update_patient_report_details(patient_report_details: schemas.PatientReportId, database: Session = Depends(get_db)):
    """Function to update particular patient report details"""
    return controller.update_patient_report_details(database, patient_report = patient_report_details)
