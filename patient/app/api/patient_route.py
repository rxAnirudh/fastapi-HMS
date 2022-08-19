"""File for patient route"""
import os
import sys
from urllib import request

from authentication import Authentication
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends, APIRouter, Form, HTTPException, Request, UploadFile,File
from sqlalchemy.orm import Session
from patient.app.models import schemas
from db import get_db

from api import controller

IMAGE_DIR_PATH = "/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/patient/patient_images"

patient_router = APIRouter()

async def create_file(file=File(None)):
    try:
        contents = await file.read()
        path = os.path.join(IMAGE_DIR_PATH, file.filename)
        with open(path, 'wb') as f:
            f.write(contents)
    finally:
        await file.close()

@patient_router.post("/add_patient")
async def add_patient(first_name: str = Form(), last_name: str = Form(), 
                      contact_number: str = Form(),
                      email: str = Form(),profile_pic: UploadFile = File(None),  gender: str = Form(),
                      date_of_birth: str = Form(default=''), blood_group: str = Form(),
                      hospital_id: int = None,marital_status: str = Form(default=''), height: str = Form(default=''), 
                      weight: str = Form(default=''),
                      emergency_contact_number: str = Form(default=''), city: str = Form(default=""),
                      allergies: str = Form(default=''), current_medications: str = Form(default=""),
                      past_injuries: str = Form(default=''),past_surgeries: str = Form(default=''), smoking_habits: str = Form(default=''), 
                      alchol_consumption: str = Form(default=''),
                      activity_level: str = Form(default=''), food_preference: str = Form(default=""),
                      occupation: str = Form(default=''),db: Session = Depends(get_db)):
    """Function to return final response while adding new patient data"""
    # Authentication().authenticate(request.headers.get('Authorization'),db)
    filename = ""
    if profile_pic is not None:
        filename = profile_pic.filename
        await create_file(profile_pic)
    return controller.add_new_patient(db, filename, first_name, last_name,
                              contact_number, email, gender, 
                              date_of_birth,blood_group,hospital_id,marital_status,height,weight, emergency_contact_number, city,
                              allergies, current_medications, past_injuries, 
                              past_surgeries,smoking_habits,alchol_consumption,activity_level,food_preference,occupation)

@patient_router.post("/get_patient_details")
def get_patient(request: Request,patientid: schemas.PatientId, database: Session = Depends(get_db)):
    """Function to return patient details
    (specific and all patient data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.get_patient_by_id(database, id = patientid.id)

@patient_router.get("/get_patient_by_pagination")
async def get_patient_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to get patient details through pagination concept"""
    return controller.get_patient_by_pagination(database,page,size)

@patient_router.post("/delete_patient_details")
def delete_patient(request: Request,patientid: schemas.PatientId, database: Session = Depends(get_db)):
    """Function to return patient details
    (specific and all patient data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.delete_patient_details(database, id = patientid.id)


@patient_router.post("/update_patient_details")
async def update_patient_report_details(request: Request,patient_id: str = Form(),profile_pic: UploadFile = File(None), first_name: str = Form(default=''), last_name: str = Form(default=''), 
                      contact_number: str = Form(default=''),
                      email: str = Form(default=''), gender: str = Form(default=""),
                      date_of_birth: str = Form(default=''), blood_group: str = Form(default=""),
                      hospital_id: str = Form(default=''),marital_status: str = Form(default=''), height: str = Form(default=''), 
                      weight: str = Form(default=''),
                      emergency_contact_number: str = Form(default=''), city: str = Form(default=""),
                      allergies: str = Form(default=''), current_medications: str = Form(default=""),
                      past_injuries: str = Form(default=''),past_surgeries: str = Form(default=''), smoking_habits: str = Form(default=''), 
                      alchol_consumption: str = Form(default=''),
                      activity_level: str = Form(default=''), food_preference: str = Form(default=""),
                      occupation: str = Form(default=''),db: Session = Depends(get_db),):
    """Function to update particular patient details"""
    # Authentication().authenticate(request.headers.get('Authorization'),db)
    filename = ""
    if profile_pic is not None:
        filename = profile_pic.filename
        await create_file(profile_pic)
    return controller.update_patient_details(db, filename, first_name, last_name,
                              contact_number, email, gender, 
                              date_of_birth,blood_group,hospital_id,marital_status,height,weight, emergency_contact_number, city,
                              allergies, current_medications, past_injuries, 
                              past_surgeries,smoking_habits,alchol_consumption,activity_level,food_preference,occupation,patient_id)