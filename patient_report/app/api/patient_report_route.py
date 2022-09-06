"""File for hospital route"""
import os
from fastapi import Depends, APIRouter, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from authentication import Authentication
from models import schemas
from db import get_db
from datetime import datetime

from api import controller

patient_report_router = APIRouter()

IMAGE_DIR_PATH = f"{os.getcwd()}/patient_report/patient_report_images"

async def create_file(file=File(None)):
    try:
        contents = await file.read()
        path = os.path.join(IMAGE_DIR_PATH, file.filename)
        with open(path, 'wb') as f:
            f.write(contents)
    finally:
        await file.close()

@patient_report_router.post("/add_new_patient_report", response_model=schemas.AddPatientReportResponse)
async def add_new_patient_report(request: Request,patient_report_file: list[UploadFile], patient_id: str = Form(default=''), report_id: str = Form(default=''), 
                      diagnose: str = Form(default=''),
                      reference: str = Form(default=''), medicine_id: str = Form(default=""),
                      medicine_name: str = Form(default=''), doctor_id: str = Form(default=""),
                      hospital_id: str = Form(default=''),db: Session = Depends(get_db)):
    """Function to return final response while adding new patient report details"""
    Authentication().authenticate(request.headers.get('Authorization'),db)
    filenames = []
    if len(patient_report_file) > 0:
      for f in patient_report_file:
          await create_file(f)
          filenames.append(f.filename)
    return controller.add_new_patient_report(db, filenames, patient_id, report_id,
                              diagnose, reference, medicine_id, 
                              medicine_name,doctor_id,hospital_id,)


@patient_report_router.post("/get_patient_report_details")
def get_patient_report_details(request: Request,patient_report_id: schemas.PatientReportId, database: Session = Depends(get_db)):
    """Function to return patient report details
    (specific and all patient report data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.get_patient_report_by_id(database, id = patient_report_id.id)


@patient_report_router.post("/delete_patient_report_details")
def delete_patient_report_details(request: Request,patient_report_id: schemas.PatientReportId, database: Session = Depends(get_db)):
    """Function to return patient report details
    (specific and all patient report data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.delete_patient_report_details(database, id = patient_report_id.id)


@patient_report_router.post("/update_patient_report_details")
async def update_patient_report_details(request: Request,patient_report_file: list[UploadFile], patient_id: str = Form(default=''), report_id: str = Form(default=''), 
                      diagnose: str = Form(default=''),
                      reference: str = Form(default=''), medicine_id: str = Form(default=""),
                      medicine_name: str = Form(default=''), doctor_id: str = Form(default=""),
                      hospital_id: str = Form(default=''),patient_report_id: str = Form(default=''),db: Session = Depends(get_db)):
    """Function to update particular patient report details"""
    Authentication().authenticate(request.headers.get('Authorization'),db)
    filenames = []
    if len(patient_report_file) > 0:
      for f in patient_report_file:
          await create_file(f)
          filenames.append(f.filename)
    return controller.update_patient_report_details(db, filenames, patient_id, report_id,
                              diagnose, reference, medicine_id, 
                              medicine_name,doctor_id,hospital_id,patient_report_id)
