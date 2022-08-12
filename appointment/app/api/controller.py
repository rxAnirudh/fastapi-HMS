import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_appointment(database: Session, appointment: schemas.AppointmentBase):
    """Function to return query based data while creating new appointment creation api"""
    if not check_if_hospital_id_is_valid(database,appointment.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    # appointment_dict = {'patient_id': appointment.dict()["patient_id"], 'hospital_id': appointment.dict()["hospital_id"],"start_time" : appointment.dict()["start_time"],
    # "end_time" : appointment.dict()["end_time"],"status_id" : appointment.dict()["status_id"],"booking_time" : appointment.dict()["booking_time"]}
    is_status_id_valid = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == appointment.dict()["status_id"]).first()
    if not is_status_id_valid:
        raise HTTPException(status_code=400, detail="status id is invalid")
    db_appointment = models.Appointment(**appointment.__dict__)
    database.add(db_appointment)
    database.commit()
    database.refresh(db_appointment)
    return ResponseData.success(db_appointment.__dict__,"Appointment booked successfully")

def get_appointment_by_id(database: Session, id : Optional[int] = None):
    """Function to get appointment details based on appointment id generated while booking new appointment"""
    db_appointment = database.query(models.Appointment).filter(models.Appointment.id == id).first()
    if db_appointment is None:
        return ResponseData.success([],"Appointment id is invalid")
    db_appointment_details = database.query(models.Appointment).filter(models.Appointment.id == id).first()
    return ResponseData.success(db_appointment_details.__dict__,"Appointment details fetched successfully")

def get_appointment_by_pagination(database: Session,page : int,size:int):
    """Function to delete single or all hospitals if needed"""
    mainData = database.query(models.Appointment).filter().all()
    if(len(mainData) > 1):
         data = mainData[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Appointment details fetched successfully")
         return ResponseData.success([],"No Appointment found")  
    return ResponseData.success(mainData,"No Appointment found")

def delete_appointment_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all appointment details if needed"""
    if id is None:
        database.query(models.Appointment).delete()
        database.commit()
        return ResponseData.success([],"All Apppointment details deleted successfully")
    database.query(models.Appointment).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Appointment details deleted successfully")

def update_appointment_details(database: Session, appointment: schemas.AddNewAppointment):
    """Function to update appointment details"""
    data = database.query(models.Appointment).filter(models.Appointment.id == appointment.id).all()
    dict1 = data[0]
    if appointment.dict()["patient_id"] is not None :
        dict1.__dict__["patient_id"] = appointment.dict()["patient_id"]
    if appointment.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = appointment.dict()["hospital_id"]
    if appointment.dict()["start_time"] is not None :
        dict1.__dict__["start_time"] = appointment.dict()["start_time"]
    if appointment.dict()["end_time"] is not None :
        dict1.__dict__["end_time"] = appointment.dict()["end_time"]
    if appointment.dict()["status_id"] is not None :
        dict1.__dict__["status_id"] = appointment.dict()["status_id"]
    if appointment.dict()["booking_time"] is not None :
        dict1.__dict__["booking_time"] = appointment.dict()["booking_time"]
    database.query(models.Appointment).filter(models.Appointment.id == appointment.id).update({ models.Appointment.id : appointment.id,
        models.Appointment.patient_id: dict1.__dict__["patient_id"],
        models.Appointment.hospital_id : dict1.__dict__["hospital_id"],
        models.Appointment.start_time : dict1.__dict__["start_time"],
        models.Appointment.end_time : dict1.__dict__["end_time"],
        models.Appointment.status_id : dict1.__dict__["status_id"],
        models.Appointment.booking_time : dict1.__dict__["booking_time"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Appointment details updated successfully")


def add_new_appointment_status(database: Session, appointment_status: schemas.AppointmentStatusBase):
    """Function to return query based data while creating new appointment status creation api"""
    appointment_status_dict = {'status': appointment_status.dict()["status"]}
    db_appointment_status = models.AppointmentStatus(**appointment_status_dict)
    database.add(db_appointment_status)
    database.commit()
    database.refresh(db_appointment_status)
    print("db_appointment_status")
    print(db_appointment_status)
    db_appointment_status.__dict__["a_id"] = db_appointment_status.a_id
    return ResponseData.success(db_appointment_status.__dict__,"Appointment status added successfully")

def get_appointment_status_by_id_or_without_id(database: Session, a_id : Optional[int] = None):
    """Function to get appointment status details"""
    if a_id is None:
        db_appointment_status_details = database.query(models.AppointmentStatus).filter().all()
        return ResponseData.success(db_appointment_status_details.__dict__,"Appointment status details fetched successfully")
    db_appointment_status = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == a_id).first()
    if db_appointment_status is None:
        return ResponseData.success([],"Appointment status id is invalid")
    db_appointment_status_details = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == a_id).first()
    return ResponseData.success(db_appointment_status_details.__dict__,"Appointment status details fetched successfully")

def delete_appointment_status(database: Session, a_id : Optional[int] = None):
    """Function to delete single or all appointment status if needed"""
    if a_id is None:
        database.query(models.AppointmentStatus).delete()
        database.commit()
        return ResponseData.success([],"All Apppointment status deleted successfully")
    database.query(models.AppointmentStatus).filter_by(a_id = a_id).delete()
    database.commit()
    return ResponseData.success([],"Appointment status deleted successfully")

def update_appointment_status_details(database: Session, appointment_status: schemas.AddNewAppointmentStatus):
    """Function to update appointment status details"""
    data = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == appointment_status.a_id).all()
    dict1 = data[0]["AppointmentStatus"]
    if appointment_status.dict()["status"] is not None :
        dict1.__dict__["status"] = appointment_status.dict()["status"]
    database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == appointment_status.a_id).update({ models.AppointmentStatus.a_id : appointment_status.a_id,
        models.AppointmentStatus.status: dict1.__dict__["status"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Appointment status details updated successfully")