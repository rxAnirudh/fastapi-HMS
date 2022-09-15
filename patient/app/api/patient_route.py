"""File for patient route"""
import os
import sys
from urllib import request
import json
from authentication import Authentication
sys.path.append(os.getcwd())
from fastapi import Depends, APIRouter, Form, HTTPException, Request, UploadFile,File
from sqlalchemy.orm import Session
from patient.app.models import schemas
from patient.app.db import get_db
from patient_report.app.db import get_db as patient_report_db
from appointment.app.db import get_db as get_appointment_db
from medicine.app.db import get_db as get_medicine_db
from patient.app.api import controller

IMAGE_DIR_PATH = f"{os.getcwd()}/patient/app/patient_images"

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
                      password: str = Form(),
                      email: str = Form(),profile_pic: UploadFile = File(None),  gender: str = Form(),
                      date_of_birth: str = Form(default=''), blood_group: str = Form(),
                      hospital_id: int = None,marital_status: str = Form(default=''), height: str = Form(default=''), 
                      weight: str = Form(default=''),
                      emergency_contact_number: str = Form(default=''), city: str = Form(default=""),
                      allergy: str = Form(default=''), current_medication: str = Form(default=""),
                      past_injury: str = Form(default=''),past_surgery: str = Form(default=''), smoking_habits: str = Form(default=''), 
                      alchol_consumption: str = Form(default=''),
                      activity_level: str = Form(default=''), food_preference: str = Form(default=""),
                      occupation: str = Form(default=''),db: Session = Depends(get_db)):
    """Function to return final response while adding new patient data"""
    filename = ""
    if profile_pic is not None:
        filename = profile_pic.filename
        await create_file(profile_pic)
    return controller.add_new_patient(db, filename, first_name, last_name,
                              contact_number,password, email, gender, 
                              date_of_birth,blood_group,hospital_id,marital_status,height,weight, emergency_contact_number, city,
                              allergy, current_medication, past_injury, 
                              past_surgery,smoking_habits,alchol_consumption,activity_level,food_preference,occupation)

import asyncio

@patient_router.post("/forget_password")
def forgot_password(request: Request,email: schemas.PatientEmail,database: Session = Depends(get_db)):
    """Function to send activation link on email id"""
    return asyncio.run(controller.patient_forget_password(database, email = email.email))

@patient_router.post("/patient_sign_in")
async def sign_in_patient(request: Request, database: Session = Depends(get_db)):
    """Function to sign in patient"""
    request_json = await request.json()
    return controller.patient_sign_in_api(database, email = request_json["email"],password = request_json["password"])

@patient_router.post("/patient_reset_password")
async def patient_reset_password(request: Request, database: Session = Depends(get_db)):
    """Function to return patient details
    (specific and all patient data can be fetched)"""
    request_json = await request.json()
    return controller.reset_password_for_patient(database,otp=request_json["otp"],new_password=request_json["new_password"])

@patient_router.post("/get_patient_details")
async def get_patient(request: Request, database: Session = Depends(get_db),appointment_database: Session = Depends(get_appointment_db),
patient_report_database: Session = Depends(patient_report_db),medicine_database: Session = Depends(get_medicine_db)):
    """Function to return patient details
    (specific and all patient data can be fetched)"""
    patientid = None
    request_json = await request.json()
    if request.headers.get('Authorization') is not None and 'doctor_id' not in request_json:
        patientid = Authentication().authenticate(request.headers.get('Authorization'),database)[0].id
    doctor_id = ''
    search = ''
    if 'doctor_id' in request_json:
        doctor_id = request_json['doctor_id']
    if 'search' in request_json:
        search = request_json['search']
    return controller.get_patient_by_id(database,appointment_database,patient_report_database,medicine_database,doctor_id,search, id = patientid)

@patient_router.get("/get_allergies")
def get_allergies(request: Request, database: Session = Depends(get_db)):
    """Function to return patient allergies
    (specific and all patient data can be fetched)"""
    return controller.get_allergies_by_id(database)

@patient_router.get("/get_food_preferences")
def get_food_preferences(request: Request, database: Session = Depends(get_db)):
    """Function to return food preferences
    (specific and all patient data can be fetched)"""
    return controller.get_food_preferences(database)

@patient_router.post("/add_allergy")
def add_allergy(request: Request,allergy_name : schemas.AllergyId, database: Session = Depends(get_db)):
    """Function to add allergy"""
    return controller.add_allergy(database,allergy_name.allergy_name)

@patient_router.post("/add_food_preference")
def add_food_preference(request: Request,food_preference_name : schemas.FoodPreferenceId, database: Session = Depends(get_db)):
    """Function to add_food_preference"""
    return controller.add_food_preference(database,food_preference_name.food_preference_name)

@patient_router.get("/get_current_medications")
def get_current_medications(database: Session = Depends(get_db)):
    """Function to return patient current_medications
    (specific and all patient data can be fetched)"""
    return controller.get_current_medication_by_id(database)

@patient_router.post("/add_current_medication")
def add_current_medication(request: Request,current_medication_name : schemas.CurrentMedicationId, database: Session = Depends(get_db)):
    """Function to add current medication"""
    return controller.add_current_medication(database,current_medication_name.current_medication_name)

@patient_router.get("/get_past_injuries")
def get_past_injuries(request: Request,database: Session = Depends(get_db)):
    """Function to return patient past injuries
    (specific and all patient data can be fetched)"""
    return controller.get_past_injuries_by_id(database)

@patient_router.post("/add_past_injury")
def add_past_injury(request: Request,past_injury : schemas.PastInjuries, database: Session = Depends(get_db)):
    """Function to add past injury"""
    return controller.add_past_injury(database,past_injury.past_injury)

@patient_router.get("/get_past_surgeries")
def get_past_surgeries(request: Request, database: Session = Depends(get_db)):
    """Function to return patient past Surgeries
    (specific and all patient data can be fetched)"""
    return controller.get_past_surgeries_by_id(database)

@patient_router.post("/add_past_surgery")
def add_past_surgery(request: Request,past_surgery : schemas.PastSurgeries, database: Session = Depends(get_db)):
    """Function to add past surgery"""
    return controller.add_past_surgery(database,past_surgery.past_surgery)

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
                      allergy: str = Form(default=''), current_medication: str = Form(default=''),
                      past_injury: str = Form(default=''),past_surgery: str = Form(default=''), smoking_habits: str = Form(default=''), 
                      alchol_consumption: str = Form(default=''),
                      activity_level: str = Form(default=''), food_preference: str = Form(default=""),
                      occupation: str = Form(default=''),db: Session = Depends(get_db),):
    """Function to update particular patient details"""
    Authentication().authenticate(request.headers.get('Authorization'),db)
    filename = ""
    if profile_pic is not None:
        filename = profile_pic.filename
        await create_file(profile_pic)
    return controller.update_patient_details(db, filename, first_name, last_name,
                              contact_number, email, gender, 
                              date_of_birth,blood_group,hospital_id,marital_status,height,weight, emergency_contact_number, city,
                              allergy, current_medication, past_injury, 
                              past_surgery,smoking_habits,alchol_consumption,activity_level,food_preference,occupation,patient_id)