"""File for hospital route"""
import os
from fastapi import Depends, APIRouter, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session
from doctor.app.models import schemas
from doctor.app.db import get_db
from patient.app.db import get_db as get_patient_db
from typing import List

from doctor.app.api import controller

doctor_router = APIRouter()
IMAGE_DIR_PATH = f"{os.getcwd()}/doctor_images"

async def create_file(file=File(None)):
    try:
        contents = await file.read()
        path = os.path.join(IMAGE_DIR_PATH, file.filename)
        with open(path, 'wb') as f:
            f.write(contents)
    finally:
        await file.close()

@doctor_router.post("/add_doctor")
async def add_doctor(
    first_name: str = Form(), last_name: str = Form(), 
                      contact_number: str = Form(),
                      email: str = Form(),profile_pic: UploadFile = Form(default = None),  gender: str = Form(),
                      date_of_birth: str = Form(default=''), blood_group: str = Form(),
                      years_of_experience: str = Form(default=''),next_available_at: str = Form(default=''), specialist_field: str = Form(default=''), 
                      education: str = Form(default=''),about: str = Form(default=''),
                      in_clinic_appointment_fees: str = Form(default=''),rating: str = Form(default=''),database: Session = Depends(get_db)):
    """Function to return final response while adding new doctor details"""
    filename = ""
    if profile_pic is not None:
        filename = profile_pic.filename
        await create_file(profile_pic)
    print("called")
    # db_doctor = controller.get_doctor(database, contact_number=doctor.contact_number)
    # if db_doctor:
    #     raise HTTPException(status_code=400, detail="Doctor already registered with same contact number")
    return controller.add_new_doctor(database,filename, first_name, last_name,
                              contact_number, email,gender,date_of_birth,blood_group,years_of_experience,next_available_at,specialist_field,education,about,in_clinic_appointment_fees,rating )


@doctor_router.post("/get_doctor_details")
async def get_doctor(request: Request,database: Session = Depends(get_db),patientDatabase: Session = Depends(get_patient_db)):
    """Function to return doctor details
    (specific and all doctor data can be fetched)"""
    request_json = await request.json()
    return controller.get_doctor_by_id(database,patientDatabase,request_json["specialist_field"])

@doctor_router.post("/get_doctor_filter")
async def get_doctor_filter(request: Request,database: Session = Depends(get_db),patientDatabase: Session = Depends(get_patient_db)):
    """Function to return doctor details
    (specific and all doctor data can be fetched)"""
    request_json = await request.json()
    return controller.get_doctor_by_filter(database,patientDatabase,request_json["specialist_field"])

@doctor_router.get("/get_doctor_by_pagination")
async def get_doctor_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to update particular doctor details"""
    return controller.get_doctor_by_pagination(database,page,size)

@doctor_router.post("/delete_doctor_details")
def delete_doctor(doctodid: schemas.DoctorId, database: Session = Depends(get_db)):
    """Function to return doctor details
    (specific and all hospitals data can be fetched)"""
    return controller.delete_doctor_details(database, id = doctodid.id)


# @doctor_router.post("/update_doctor_details")
# def update_doctor_details(doctor_details: schemas.AddNewDoctor, database: Session = Depends(get_db)):
#     """Function to update particular doctor details"""
#     return controller.update_doctor_details(database, doctor = doctor_details)

@doctor_router.post("/update_doctor_details")
async def update_doctor_detail(request: Request,doctor_id: str = Form(),first_name: str = Form(default=''), last_name: str = Form(default=''), 
                      contact_number: str = Form(default=''),
                      email: str = Form(default=''),profile_pic: UploadFile = File(None),  gender: str = Form(default=''),
                      date_of_birth: str = Form(default=''), blood_group: str = Form(default=''),
                      years_of_experience: str = Form(default=''),next_available_at: str = Form(default=''), specialist_field: str = Form(default=''), 
                      education: str = Form(default=''),about: str = Form(default=''),
                      in_clinic_appointment_fees: str = Form(default=''),rating: str = Form(default=''),database: Session = Depends(get_db)):
    """Function to update particular doctor details"""
    # Authentication().authenticate(request.headers.get('Authorization'),db)
    filename = ""
    if profile_pic is not None:
        filename = profile_pic.filename
        await create_file(profile_pic)
    return controller.update_doctor_details(database,filename, first_name, last_name,
                              contact_number, email,gender,date_of_birth,blood_group,years_of_experience,next_available_at,specialist_field,education,about,in_clinic_appointment_fees,rating,doctor_id)

@doctor_router.post("/add_doctor_feedback")
async def add_doctor_feedback(request: Request,database: Session = Depends(get_db),patientDatabase: Session = Depends(get_patient_db)):
    """Function to add doctor feedback"""
    request_json = await request.json()
    return controller.add_feeback_of_doctor(database,patientDatabase,comment = request_json["comment"],rating = request_json["rating"],patient_id = request_json["patient_id"],
    staff_id = request_json["staff_id"],doctor_id = request_json["doctor_id"],hospital_id = request_json["hospital_id"],)