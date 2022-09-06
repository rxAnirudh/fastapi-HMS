"""File for hospital route"""
import os
from fastapi import Depends, APIRouter, File, Form, Request, UploadFile
from sqlalchemy.orm import Session
from authentication import Authentication
from appointment.app.models import schemas
from appointment.app.db import get_db
from doctor.app.db import get_db as get_doctor_db
from patient.app.db import get_db as get_patient_db

from appointment.app.api import controller

appointment_router = APIRouter()

IMAGE_DIR_PATH = f"{os.getcwd()}/appointment_files"
PROFILE_DIR_PATH = f"{os.getcwd()}/patient_profile_pic_files"

async def create_file(file=File(None),filepath=str):
    print(f"os. getcwd() {os.getcwd()}")
    try:
        contents = await file.read()
        path1 = os.path.join(filepath, file.filename)
        with open(path1, 'wb') as f:
            f.write(contents)
    finally:
        await file.close()

@appointment_router.post("/add_new_appointment")
async def add_new_appointment(first_name: str = Form(), last_name: str = Form(), 
                      mobile_number: str = Form(),
                      booking_time: str = Form(),
                      status_id: str = Form(default=''),file_data: UploadFile = Form(default=None),
                      hospital_id: str = Form(default=''),patient_id: str = Form(), doctor_id: str = Form(),time_slot: str = Form(), 
                      staff_id: str = Form(default=''),
                      patient_profile_pic: UploadFile = Form(default=None),
                      disease :str = Form(default=''),
                      appointment_date: str = Form(),
                      db: Session = Depends(get_db),patient_db: Session = Depends(get_patient_db)):
    """Function to return final response while adding new appointment data"""
    # Authentication().authenticate(request.headers.get('Authorization'),db)
    filename = ""
    profile_pic = ""
    if file_data is not None:
        filename = file_data.filename
        await create_file(file_data,IMAGE_DIR_PATH)
    if patient_profile_pic is not None:
        profile_pic = patient_profile_pic.filename
        await create_file(patient_profile_pic,PROFILE_DIR_PATH)
    return controller.add_new_appointment(db, patient_db,first_name, last_name,
                              mobile_number,booking_time, status_id, hospital_id, 
                              patient_id,doctor_id,staff_id,filename,profile_pic,time_slot,disease,appointment_date)


@appointment_router.post("/get_appointment_details")
async def get_appointment_details(request:Request, database: Session = Depends(get_db),patient_db: Session = Depends(get_patient_db),doctor_database: Session = Depends(get_doctor_db)):
    """Function to return Appointment details
    (specific and all Appointment data can be fetched)"""
    # patient_id = Authentication().authenticate(request.headers.get('Authorization'),database)[0].id
    request_json = await request.json()
    return controller.get_appointment_by_id(database,patient_db,request_json["id"],request_json["date"],doctor_database)

@appointment_router.post("/get_appointment_by_date")
async def get_appointment_details_by_date(request:Request, database: Session = Depends(get_db),doctor_database: Session = Depends(get_doctor_db)):
    """Function to return Appointment details based on appointment date
    (specific and all Appointment data can be fetched)"""
    # patient_id = Authentication().authenticate(request.headers.get('Authorization'),database)[0].id
    request_json = await request.json()
    return controller.get_appointment_by_date(database,request_json["appointment_date"],doctor_database)

@appointment_router.post("/delete_appointment_details")
def delete_appointment_details(request:Request,appointment_id: schemas.AppointmentId, database: Session = Depends(get_db)):
    """Function to return Appointment details
    (specific and all Appointment data can be fetched)"""
    # Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.delete_appointment_details(database, id = appointment_id.id)

# @appointment_router.post("/update_appointment_details")
# def update_appointment_details(request:Request,appointment_details: schemas.AddNewAppointment, database: Session = Depends(get_db)):
#     """Function to update particular Appointment details"""
#     Authentication().authenticate(request.headers.get('Authorization'),database)
#     return controller.update_appointment_details(database, appointment = appointment_details)

# @appointment_router.post("/update_appointment_details")
# def update_appointment_details(request:Request,appointment_details: schemas.AddNewAppointment, database: Session = Depends(get_db)):
#     """Function to update particular Appointment details"""
#     Authentication().authenticate(request.headers.get('Authorization'),database)
#     return controller.update_appointment_details(database, appointment = appointment_details)

@appointment_router.post("/update_appointment_details")
async def update_appointment_details(request: Request,appointment_id: str = Form(),first_name: str = Form(), last_name: str = Form(), 
                      mobile_number: str = Form(),
                      booking_time: str = Form(),
                      status_id: str = Form(default=''),file_data: UploadFile = Form(default=None),patient_profile_pic: UploadFile = Form(default=None),
                      hospital_id: str = Form(default=''),patient_id: str = Form(default=''), doctor_id: str = Form(), 
                      staff_id: str = Form(default=''),
                      time_slot: str = Form(default=''),appointment_date: str = Form(default=''),
                      db: Session = Depends(get_db),doctor_database: Session = Depends(get_doctor_db)):
    """Function to update particular appointment detail"""
    # Authentication().authenticate(request.headers.get('Authorization'),db)
    filename = ""
    profile_pic = ""
    if file_data is not None:
        filename = file_data.filename
        await create_file(file_data,IMAGE_DIR_PATH)
    if patient_profile_pic is not None:
        profile_pic = patient_profile_pic.filename
        await create_file(patient_profile_pic,PROFILE_DIR_PATH)
    return controller.update_appointment_details(db,doctor_database, first_name, last_name,
                              mobile_number,booking_time, status_id, hospital_id, 
                              patient_id,doctor_id,staff_id,filename,profile_pic,appointment_id,time_slot,appointment_date)

@appointment_router.get("/get_appointment_by_pagination")
async def get_appointment_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to update particular hospital details"""
    return controller.get_appointment_by_pagination(database,page,size)

@appointment_router.post("/add_appointment_status", response_model=schemas.AddAppointmentStatusResponse)
def add_appointment_status(appointment_status: schemas.AppointmentStatusBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new Appointment status details"""
    return controller.add_new_appointment_status(database,appointment_status)


@appointment_router.post("/get_appointment_status")
def get_appointment_status(appointment_status_id: schemas.AppointmentStatusId, database: Session = Depends(get_db)):
    """Function to return Appointment details
    (specific and all Appointment status data can be fetched)"""
    return controller.get_appointment_status_by_id_or_without_id(database, id = appointment_status_id.id)


@appointment_router.post("/delete_appointment_status")
def delete_appointment_status(appointment_status_id: schemas.AppointmentStatusId, database: Session = Depends(get_db)):
    """Function to return Appointment details
    (specific and all Appointment data can be fetched)"""
    return controller.delete_appointment_status(database, id = appointment_status_id.id)


@appointment_router.post("/update_appointment_status")
def update_appointment_status(appointment_status: schemas.AddNewAppointmentStatus, database: Session = Depends(get_db)):
    """Function to update particular Appointment status details"""
    return controller.update_appointment_status_details(database, appointment_status = appointment_status)
