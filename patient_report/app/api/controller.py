import sys
import os
from fastapi import HTTPException
from sqlalchemy import INTEGER, Integer
sys.path.append(os.getcwd())
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from patient_report.app.models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.api.controller import check_if_patient_id_is_valid
from doctor.app.api.controller import check_if_doctor_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_patient_report(database: Session, file: list(), patient_id: str, report_id: str, diagnose: str,
                      reference: str, medicine_id: str,
                      medicine_name: str, doctor_id: str,
                      hospital_id: str):
    """Function to add new patient report details"""
    if not check_if_hospital_id_is_valid(database,hospital_id):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_patient_id_is_valid(database,patient_id):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    if not check_if_doctor_id_is_valid(database,doctor_id):
        raise HTTPException(status_code=400, detail="Doctor id is invalid")
    filedata = ''
    for i in file:
        if len(file) == 1:
           filedata+=i
        elif len(file) > 1:
           filedata+=i+','
    patientreportdata = {
        "patient_id": patient_id,
  "report_id": report_id,
  "diagnose": diagnose,
  "reference": reference,
  "medicine_id": medicine_id,
  "medicine_name": medicine_name,
  "doctor_id": doctor_id,
  "hospital_id": hospital_id,
  'patient_report_file' : filedata
    }
    db_patient_report = models.PatientReport(**patientreportdata)
    database.add(db_patient_report)
    database.commit()
    database.refresh(db_patient_report)
    return ResponseData.success(db_patient_report.__dict__,"New Patient report generated successfully")

def get_patient_report_by_id(database: Session, id : Optional[int] = None):
    """Function to get patient report details based on patient report id generated while adding new patient report"""
    if id is None:
        db_patient_report = database.query(models.PatientReport).filter().first()
        if db_patient_report is None:
            return ResponseData.success([],"No patient report data exists in database")
        return ResponseData.success(db_patient_report.__dict__,"Patient report details fetched successfully")
    db_patient_report = database.query(models.PatientReport).filter(models.PatientReport.id == id).first()
    if db_patient_report is None:
        return ResponseData.success([],"Patient report id is invalid")
    return ResponseData.success(db_patient_report.__dict__,"Patient report details fetched successfully")

def delete_patient_report_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all patient report details if needed"""
    if id is None:
        database.query(models.PatientReport).delete()
        database.commit()
        return ResponseData.success([],"All patient report details deleted successfully")
    database.query(models.PatientReport).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Patient report details deleted successfully")

def update_patient_report_details(database: Session, file: list(), patient_id: str, report_id: str, diagnose: str,
                      reference: str, medicine_id: str,
                      medicine_name: str, doctor_id: str,
                      hospital_id: str,patient_report_id: Integer):
    """Function to update patient report details"""
    data = database.query(models.PatientReport).filter(models.PatientReport.id == patient_report_id).all()
    dict1 = data[0]
    if patient_id != '' :
        dict1.__dict__["patient_id"] = patient_id
    if len(file) > 0 :
        filedata = ''
        for i in file:
            if len(file) == 1:
               filedata+='{0}'.format(i)
            elif len(file) > 1:
               filedata+='{i},'.format(i)
        dict1.__dict__["patient_report_file"] = filedata
    if report_id != '' :
        dict1.__dict__["report_id"] = report_id
    if diagnose != '' :
        dict1.__dict__["diagnose"] = diagnose
    if reference != '' :
        dict1.__dict__["reference"] = reference
    if medicine_id != '' :
        dict1.__dict__["medicine_id"] = medicine_id
    if medicine_name != '' :
        dict1.__dict__["medicine_name"] = medicine_name
    if doctor_id != '' :
        dict1.__dict__["doctor_id"] = doctor_id
    if hospital_id != '' :
        dict1.__dict__["hospital_id"] = hospital_id
    if patient_report_id != '' :
        dict1.__dict__["patient_report_id"] = patient_report_id
    database.query(models.PatientReport).filter(models.PatientReport.id == patient_report_id).update({ models.PatientReport.id : patient_report_id,
        models.PatientReport.patient_id: dict1.__dict__["patient_id"],
        models.PatientReport.report_id : dict1.__dict__["report_id"],
        models.PatientReport.diagnose : dict1.__dict__["diagnose"],
        models.PatientReport.reference : dict1.__dict__["reference"],
        models.PatientReport.medicine_id : dict1.__dict__["medicine_id"],
        models.PatientReport.medicine_name : dict1.__dict__["medicine_name"],
        models.PatientReport.doctor_id : dict1.__dict__["doctor_id"],
        models.PatientReport.hospital_id : dict1.__dict__["hospital_id"],
        models.PatientReport.patient_report_file : dict1.__dict__["patient_report_file"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Patient Report details updated successfully")

