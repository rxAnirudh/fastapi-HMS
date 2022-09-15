import os
import sys

from fastapi import HTTPException, UploadFile
from sqlalchemy import Integer

import patient

sys.path.append({os.getcwd()})
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from appointment.app.models import models,schemas
from doctor.app.models import models as doctorModels
from medicine.app.models import models as medicineModels
from patient.app.models import models as patientModels
from patient_report.app.models import models as PatientReportModels
from appointment.app.response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from appointment.app.error_handling import Error
from patient.app.api.controller import check_if_patient_id_is_valid



# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_appointment(database: Session,patientDatabase: Session,doctorDatabase:Session, first_name: str, last_name: str, mobile_number: str,booking_time: str,
                       hospital_id: str,
                      patient_id: str, doctor_id: str,staff_id: str,file : UploadFile,profile_pic: UploadFile,time_slot: str,disease: str,appointment_date: str):
    """Function to add new appointment data"""
    # db_patient_number = database.query(models.Appointment).filter(models.Appointment.mobile_number == mobile_number).first()
    # if not db_patient_number:
    #     return ResponseData.success_without_data("Mobile number entered is not valid")
    db_patient_id = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(patient_id)).first()
    db_doctor_id = doctorDatabase.query(doctorModels.Doctor).filter(doctorModels.Doctor.id == int(doctor_id)).first()
    status = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.status == 'Pending').first()
    status_id = ''
    if status:
        status_id = str(status.a_id)
    if not db_patient_id:
        return ResponseData.success_without_data("Patient id is invalid")
    if not db_doctor_id:
        return ResponseData.success_without_data("Doctor id is invalid")
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

def get_appointment_by_id(database: Session,patient_report_database: Session,patientDatabase: Session,patient_id,doctor_id,date,get_doctor_database: Session,medicine_database : Session):
    """Function to get appointment details based on appointment id generated while booking new appointment"""
    if doctor_id == "":
       db_patient_id = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == patient_id).first()
       if not db_patient_id:
           return ResponseData.error("Patient id is invalid")
       if date == "":
          db_appointment = database.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()
       else:
          db_appointment = database.query(models.Appointment).filter(models.Appointment.patient_id == patient_id,models.Appointment.appointment_date == date).all()
       if len(db_appointment) == 0 and date == "":
           return ResponseData.success([],"No appointment found for this patient")
       if len(db_appointment) == 0 and date != "":
           return ResponseData.success([],"No appointment found for this date")
    else:
       db_doctor_id = get_doctor_database.query(doctorModels.Doctor).filter(doctorModels.Doctor.id == int(doctor_id)).first()
       if not db_doctor_id:
           return ResponseData.error("Doctor id is invalid")
       if date == "":
          db_appointment = database.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()
       else:
          db_appointment = database.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id,models.Appointment.appointment_date == date).all()
       if len(db_appointment) == 0 and date == "":
           return ResponseData.success([],"No appointment found for this patient")
       if len(db_appointment) == 0 and date != "":
           return ResponseData.success([],"No appointment found for this date")
    for i in range(0,len(db_appointment)):
     db_doctor = get_doctor_database.query(doctorModels.DoctorDetails,doctorModels.Doctor).filter(doctorModels.Doctor.id == doctorModels.DoctorDetails.id,doctorModels.Doctor.id == db_appointment[i].doctor_id).first()
     if db_doctor is not None:
         dict1 = db_doctor["DoctorDetails"]
         dict2 = db_doctor["Doctor"]
         dict1.__dict__.update(dict2.__dict__)
         print(f"dict2.__dict__ {dict1.__dict__}")
         db_appointment[i].__dict__["doctor_data"] = dict1.__dict__
         db_appointment[i].__dict__.pop("doctor_id")
         db_patient_report = patient_report_database.query(PatientReportModels.PatientReport).filter(PatientReportModels.PatientReport.appointment_id == str(db_appointment[i].__dict__["id"])).first()
         if db_patient_report:
             db_appointment[i].__dict__["patient_report_data"] = db_patient_report.__dict__
         # else:
         #     db_appointment[i].__dict__["patient_report_data"] = db_patient_report.__dict__
         db_patient_updated_report_medicine_details = patient_report_database.query(PatientReportModels.PatientReportMedicineDetails).filter().all()
         for j in range(0,len(db_patient_updated_report_medicine_details)):
             print(f'db_patient_updated_report_medicine_details[i].__dict__["medicine_id"] {db_patient_updated_report_medicine_details[j].__dict__["medicine_id"]}')
             medicine_name = medicine_database.query(medicineModels.Medicine).filter((medicineModels.Medicine.id == int(db_patient_updated_report_medicine_details[j].__dict__["medicine_id"]))).first()
             if not medicine_name:
                 return ResponseData.error("medicine id is invalid")
             db_patient_updated_report_medicine_details[j].__dict__["medicine_name"] = medicine_name.name
             db_patient_updated_report_medicine_details[j].__dict__.pop("medicine_id")
         if db_patient_report:
           db_appointment[i].__dict__["patient_report_data"]["medicine_details"] = db_patient_updated_report_medicine_details
    return ResponseData.success(db_appointment,"Appointment details fetched successfully")

def get_appointment_by_date(database: Session,date,get_doctor_database: Session):
    """Function to get appointment details based on appointment id generated while booking new appointment"""
    db_appointment = database.query(models.Appointment).filter(models.Appointment.appointment_date == date).all()
    if len(db_appointment) == 0:
        return ResponseData.error("patient id is invalid")
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
def update_appointment_details(database: Session,patient_report_database: Session,get_doctor_database: Session, medicine_database: Session,first_name: str, last_name: str, mobile_number: str,booking_time: str,
                      status_id: str, hospital_id: str,
                      patient_id: str, doctor_id: str,staff_id: str,file : UploadFile,profile_pic: UploadFile, report_description:str,medicine_id:str,patient_report_file:str,appointment_id: Integer,time_slot: str,appointment_date: str):
    """Function to update appointment details"""
    db_appointment = database.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        return ResponseData.success_without_data("Appointment with this id does not exists")
    status = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == int(status_id)).first()
    if not status:
        return ResponseData.success_without_data("Status with this id does not exists")
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
    db_patient_report_details = patient_report_database.query(PatientReportModels.PatientReport).filter(PatientReportModels.PatientReport.appointment_id == str(appointment_id)).first()
    if not db_patient_report_details:
       patientreportdata = {
        "patient_id": db_appointment_updated.patient_id,
  "report_description": report_description,
  "doctor_id": db_appointment_updated.doctor_id,
  "hospital_id": db_appointment_updated.hospital_id,
  "appointment_id" : db_appointment_updated.id
       }
       db_patient_report = PatientReportModels.PatientReport(**patientreportdata)
       patient_report_database.add(db_patient_report)
       patient_report_database.commit()
       patient_report_database.refresh(db_patient_report)
       medicine_list = medicine_id.split(",")
       patientreportmedicinedata = {
            "patient_id": db_appointment_updated.patient_id,
  "medicine_id": "",
           }
       print(f"medicine_list {medicine_list}")
       for i in range(0,len(medicine_list)):
           patientreportmedicinedata["medicine_id"] = medicine_list[i],
           db_patient_report_medicine_data = patient_report_database.query(PatientReportModels.PatientReportMedicineDetails).filter(PatientReportModels.PatientReportMedicineDetails.medicine_id == medicine_list[i]).first()
           if not db_patient_report_medicine_data:
            db_patient_report_medicine_details = PatientReportModels.PatientReportMedicineDetails(**patientreportmedicinedata)
            patient_report_database.add(db_patient_report_medicine_details)
            patient_report_database.commit()
            patient_report_database.refresh(db_patient_report_medicine_details)
    else:
        dict2 = {
        "patient_id": patient_id if patient_id != "" else db_patient_report_details.patient_id,
  "report_description": report_description if report_description != "" else db_patient_report_details.report_description,
  "doctor_id": doctor_id if doctor_id != "" else db_patient_report_details.doctor_id,
  "hospital_id": hospital_id if hospital_id != "" else db_patient_report_details.hospital_id,
    }
        for key,value in dict2.items():
           update_fields(dict2,key,value)
        patient_report_database.query(PatientReportModels.PatientReport).filter(PatientReportModels.PatientReport.id == db_patient_report_details.id).update({PatientReportModels.PatientReport.id : db_patient_report_details.id,
        PatientReportModels.PatientReport.patient_id: dict2["patient_id"],
        PatientReportModels.PatientReport.report_description: dict2["report_description"],
        PatientReportModels.PatientReport.doctor_id: dict2["doctor_id"],
        PatientReportModels.PatientReport.hospital_id: dict2["hospital_id"],
    })
        patient_report_database.flush()
        patient_report_database.commit()
        medicine_list = medicine_id.split(",")
        patient_report_database.query(PatientReportModels.PatientReportMedicineDetails).delete()
        for i in range(0,len(medicine_list)):
           dict3 = {
        "patient_id": patient_id if patient_id != "" else db_patient_report_details.patient_id,
    }
           for key,value in dict3.items():
              update_fields(dict3,key,value)
           patientreportmedicinedata = {
            "patient_id": db_appointment_updated.patient_id,
  "medicine_id": medicine_list[i],
           }
           db_patient_report_medicine_details = PatientReportModels.PatientReportMedicineDetails(**patientreportmedicinedata)
           patient_report_database.add(db_patient_report_medicine_details)
           patient_report_database.commit()
           patient_report_database.refresh(db_patient_report_medicine_details)
    db_patient_updated_report_details = patient_report_database.query(PatientReportModels.PatientReport).filter(PatientReportModels.PatientReport.appointment_id == str(appointment_id)).first()
    db_appointment_updated.__dict__["patient_report_data"] = db_patient_updated_report_details.__dict__
    db_patient_updated_report_medicine_details = patient_report_database.query(PatientReportModels.PatientReportMedicineDetails).filter().all()
    for i in range(0,len(db_patient_updated_report_medicine_details)):
        print(f'db_patient_updated_report_medicine_details[i].__dict__["medicine_id"] {db_patient_updated_report_medicine_details[i].__dict__["medicine_id"]}')
        medicine_name = medicine_database.query(medicineModels.Medicine).filter((medicineModels.Medicine.id == int(db_patient_updated_report_medicine_details[i].__dict__["medicine_id"]))).first()
        if not medicine_name:
            return ResponseData.error("medicine id is invalid")
        db_patient_updated_report_medicine_details[i].__dict__["medicine_name"] = medicine_name.name
        db_patient_updated_report_medicine_details[i].__dict__.pop("medicine_id")
    db_appointment_updated.__dict__["patient_report_data"]["medicine_details"] = db_patient_updated_report_medicine_details
    db_doctor = get_doctor_database.query(doctorModels.DoctorDetails,doctorModels.Doctor).filter(doctorModels.Doctor.id == db_appointment_updated.doctor_id).first()
    print(f"db_doctor {db_doctor}")
    if db_doctor is not None:
       dict1 = db_doctor["DoctorDetails"]
       dict2 = db_doctor["Doctor"]
       dict1.__dict__.update(dict2.__dict__)
       db_appointment_updated.__dict__["doctor_data"] = dict1.__dict__
       db_appointment_updated.__dict__.pop("doctor_id")
    return ResponseData.success(db_appointment_updated,"Appointment details updated successfully")


def add_new_appointment_status(database: Session, appointment_status):
    """Function to return query based data while creating new appointment status creation api"""
    appointment_status_dict = {'status': appointment_status}
    db_appointment_status = models.AppointmentStatus(**appointment_status_dict)
    database.add(db_appointment_status)
    database.commit()
    database.refresh(db_appointment_status)
    print("db_appointment_status")
    print(db_appointment_status)
    db_appointment_status.__dict__["a_id"] = db_appointment_status.a_id
    return ResponseData.success(db_appointment_status.__dict__,"Appointment status added successfully")

def get_appointment_status_by_id_or_without_id(database: Session, id):
    """Function to get appointment status details"""
    if id  == "":
        db_appointment_status_details = database.query(models.AppointmentStatus).filter().all()
        return ResponseData.success(db_appointment_status_details,"Appointment status details fetched successfully")
    db_appointment_status = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == id).first()
    if db_appointment_status is None:
        return ResponseData.success([],"Appointment status id is invalid")
    db_appointment_status_details = database.query(models.AppointmentStatus).filter(models.AppointmentStatus.a_id == id).first()
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