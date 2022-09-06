import os
import sys

from fastapi import HTTPException, UploadFile
from sqlalchemy import Integer

sys.path.append({os.getcwd()})
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from appointment.app.models import models,schemas
from doctor.app.models import models as doctorModels
from patient.app.models import models as patientModels
from appointment.app.response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from appointment.app.error_handling import Error
from patient.app.api.controller import check_if_patient_id_is_valid



# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_appointment(database: Session,patientDatabase: Session, first_name: str, last_name: str, mobile_number: str,booking_time: str,
                      status_id: str, hospital_id: str,
                      patient_id: str, doctor_id: str,staff_id: str,file : UploadFile,profile_pic: UploadFile,time_slot: str,disease: str,appointment_date: str):
    """Function to add new appointment data"""
    # db_patient_number = database.query(models.Appointment).filter(models.Appointment.mobile_number == mobile_number).first()
    # if not db_patient_number:
    #     return ResponseData.success_without_data("Mobile number entered is not valid")
    db_patient_id = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(patient_id)).first()
    if not db_patient_id:
        return ResponseData.success_without_data("Patient id is invalid")
    appointment_data = {
        "first_name": first_name,
  "last_name": last_name,
  "mobile_number": mobile_number,
  "booking_time" : booking_time,
  "status_id": status_id,
  "hospital_id": hospital_id,
  "patient_id": patient_id,
  "doctor_id": doctor_id,
  "staff_id": staff_id,
  "time_slot": time_slot,
  "appointment_date": appointment_date,
  'file_data' : f'appointment/app/appointment_files/{file}' if file != "" else "",
  'patient_profile_pic' : f'patient/app/patient_profile_pic_files/{profile_pic}' if profile_pic != "" else "",
  "disease": disease,
    }
    db_appointment = models.Appointment(**appointment_data)
    database.add(db_appointment)
    database.commit()
    database.refresh(db_appointment)
    return ResponseData.success(db_appointment.__dict__,"Appointment booked successfully")

def get_appointment_by_id(database: Session,patientDatabase: Session,patient_id,date,get_doctor_database: Session):
    """Function to get appointment details based on appointment id generated while booking new appointment"""
    print(f"patient_id {patient_id}")
    db_patient_id = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(patient_id)).first()
    if not db_patient_id:
        return ResponseData.success_without_data("Patient id is invalid")
    if date == "":
       db_appointment = database.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()
    else:
       db_appointment = database.query(models.Appointment).filter(models.Appointment.patient_id == patient_id,models.Appointment.appointment_date == date).all()
    if len(db_appointment) == 0 and date == "":
        return ResponseData.success([],"No appointment found for this patient")
    if len(db_appointment) == 0 and date != "":
        return ResponseData.success([],"No appointment found for this date")
    db_doctor = get_doctor_database.query(doctorModels.DoctorDetails,doctorModels.Doctor).filter(doctorModels.Doctor.id == db_appointment[0].doctor_id).first()
    if db_doctor is not None:
       dict1 = db_doctor["DoctorDetails"]
       dict2 = db_doctor["Doctor"]
       dict1.__dict__.update(dict2.__dict__)
       print(f"dict2.__dict__ {dict1.__dict__}")
       for i in range(0,len(db_appointment)):
        db_appointment[i].__dict__["doctor_data"] = dict1.__dict__
        db_appointment[i].__dict__.pop("doctor_id")
    #    Merge(db_doctor.__dict__,db_appointment.__dict__)
    return ResponseData.success(db_appointment,"Appointment details fetched successfully")

def get_appointment_by_date(database: Session,date,get_doctor_database: Session):
    """Function to get appointment details based on appointment id generated while booking new appointment"""
    db_appointment = database.query(models.Appointment).filter(models.Appointment.appointment_date == date).all()
    if len(db_appointment) == 0:
        return ResponseData.success([],"patient id is invalid")
    db_doctor = get_doctor_database.query(doctorModels.DoctorDetails,doctorModels.Doctor).filter(doctorModels.Doctor.id == db_appointment[0].doctor_id).first()
    if db_doctor is not None:
       dict1 = db_doctor["DoctorDetails"]
       dict2 = db_doctor["Doctor"]
       dict1.__dict__.update(dict2.__dict__)
       print(f"dict2.__dict__ {dict1.__dict__}")
       for i in range(0,len(db_appointment)):
        db_appointment[i].__dict__["doctor_data"] = dict1.__dict__
        db_appointment[i].__dict__.pop("doctor_id")
    #    Merge(db_doctor.__dict__,db_appointment.__dict__)
    return ResponseData.success(db_appointment,"Appointment details fetched successfully")

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

def update_fields(actualDict,key,value):
    if key != '' or key is not None:
        actualDict[f"{key}"] = value
def update_appointment_details(database: Session,get_doctor_database: Session, first_name: str, last_name: str, mobile_number: str,booking_time: str,
                      status_id: str, hospital_id: str,
                      patient_id: str, doctor_id: str,staff_id: str,file : UploadFile,profile_pic: UploadFile, appointment_id: Integer,time_slot: str,appointment_date: str):
    """Function to update appointment details"""
    db_appointment = database.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        return ResponseData.success_without_data("Appointment with this id does not exists")
    dict1 = {
        "first_name": first_name if first_name != "" else db_appointment.first_name,
  "last_name": last_name if last_name != "" else db_appointment.last_name,
  "mobile_number": mobile_number if mobile_number != "" else db_appointment.mobile_number,
  "booking_time": booking_time if booking_time != "" else db_appointment.booking_time,
  "hospital_id": hospital_id if hospital_id != "" else db_appointment.hospital_id,
  "doctor_id": doctor_id if doctor_id != "" else db_appointment.doctor_id,
  "patient_id": patient_id if patient_id != "" else db_appointment.patient_id,
  "staff_id": staff_id if staff_id != "" else db_appointment.staff_id,
  "status_id": status_id if status_id != "" else db_appointment.status_id,
  "time_slot": time_slot if time_slot != "" else db_appointment.time_slot,
  "appointment_date": appointment_date if appointment_date != "" else db_appointment.appointment_date,
  'file_data' : f"appointment/app/appointment_files/{file}" if file != "" else f"{db_appointment.file_data}",
  'patient_profile_pic' : f"patient/app/patient_profile_pic_files/{profile_pic}" if profile_pic != "" else f"{db_appointment.patient_profile_pic}",
    }
    for key,value in dict1.items():
        update_fields(dict1,key,value)
    database.query(models.Appointment).filter(models.Appointment.id == appointment_id).update({models.Appointment.id : appointment_id,
        models.Appointment.first_name: dict1["first_name"],
        models.Appointment.last_name : dict1["last_name"],
        models.Appointment.mobile_number : dict1["mobile_number"],
        models.Appointment.booking_time : dict1["booking_time"],
        models.Appointment.hospital_id : dict1["hospital_id"],
        models.Appointment.doctor_id : dict1["doctor_id"],
        models.Appointment.patient_id : dict1["patient_id"],
        models.Appointment.staff_id : dict1["staff_id"],
        models.Appointment.status_id : dict1["status_id"],
        models.Appointment.time_slot : dict1["time_slot"],
        models.Appointment.appointment_date : dict1["appointment_date"],
        models.Appointment.file_data : dict1["file_data"],
      models.Appointment.patient_profile_pic : dict1["patient_profile_pic"],  
    })
    database.flush()
    database.commit()
    db_appointment_updated = database.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    db_doctor = get_doctor_database.query(doctorModels.DoctorDetails,doctorModels.Doctor).filter(doctorModels.Doctor.id == db_appointment_updated.doctor_id).first()
    if db_doctor is not None:
       dict1 = db_doctor["DoctorDetails"]
       dict2 = db_doctor["Doctor"]
       dict1.__dict__.update(dict2.__dict__)
       db_appointment_updated.__dict__["doctor_data"] = dict1.__dict__
       db_appointment_updated.__dict__.pop("doctor_id")
    return ResponseData.success(db_appointment_updated,"Appointment details updated successfully")


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