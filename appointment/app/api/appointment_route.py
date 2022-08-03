"""File for hospital route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import schemas
from db import get_db

from api import controller

appointment_router = APIRouter()


@appointment_router.post("/add_new_appointment", response_model=schemas.AddAppointmentResponse)
def add_new_appointment(appointment: schemas.AppointmentBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new Appointment details"""
    return controller.add_new_appointment(database,appointment)


@appointment_router.post("/get_appointment_details")
def get_appointment_details(appointmentid: schemas.AppointmentId, database: Session = Depends(get_db)):
    """Function to return Appointment details
    (specific and all Appointment data can be fetched)"""
    return controller.get_appointment_by_id(database, id = appointmentid.id)


@appointment_router.post("/delete_appointment_details")
def delete_appointment_details(appointmentid: schemas.AppointmentId, database: Session = Depends(get_db)):
    """Function to return Appointment details
    (specific and all Appointment data can be fetched)"""
    return controller.delete_appointment_details(database, id = appointmentid.id)


@appointment_router.post("/update_appointment_details")
def update_appointment_details(appointment_details: schemas.AddNewAppointment, database: Session = Depends(get_db)):
    """Function to update particular Appointment details"""
    return controller.update_appointment_details(database, appointment = appointment_details)


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