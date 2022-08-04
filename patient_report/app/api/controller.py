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
from patient.app.api.controller import check_if_patient_id_is_valid
from doctor.app.api.controller import check_if_doctor_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_patient_report(database: Session, patientreport: schemas.PatientReportBase):
    """Function to add new patient report details"""
    if not check_if_hospital_id_is_valid(database,patientreport.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_patient_id_is_valid(database,patientreport.dict()["patient_id"]):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    if not check_if_doctor_id_is_valid(database,patientreport.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Doctor id is invalid")
    db_patient_report = models.Supplier(**patientreport.__dict__)
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

def update_patient_report_details(database: Session, patient_report: schemas.AddNewPatientReport):
    """Function to update patient report details"""
    data = database.query(models.PatientReport).filter(models.PatientReport.id == patient_report.id).all()
    dict1 = data[0]
    if patient_report.dict()["patient_id"] is not None :
        dict1.__dict__["patient_id"] = patient_report.dict()["patient_id"]
    if patient_report.dict()["report_id"] is not None :
        dict1.__dict__["report_id"] = patient_report.dict()["report_id"]
    if patient_report.dict()["diagnose"] is not None :
        dict1.__dict__["diagnose"] = patient_report.dict()["diagnose"]
    if patient_report.dict()["reference"] is not None :
        dict1.__dict__["reference"] = patient_report.dict()["reference"]
    if patient_report.dict()["medicine_id"] is not None :
        dict1.__dict__["medicine_id"] = patient_report.dict()["medicine_id"]
    if patient_report.dict()["medicine_name"] is not None :
        dict1.__dict__["medicine_name"] = patient_report.dict()["medicine_name"]
    if patient_report.dict()["doctor_id"] is not None :
        dict1.__dict__["doctor_id"] = patient_report.dict()["doctor_id"]
    if patient_report.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = patient_report.dict()["hospital_id"]
    
    database.query(models.PatientReport).filter(models.PatientReport.id == patient_report.id).update({ models.PatientReport.id : patient_report.id,
        models.PatientReport.patient_id: dict1.__dict__["patient_id"],
        models.PatientReport.report_id : dict1.__dict__["report_id"],
        models.PatientReport.diagnose : dict1.__dict__["diagnose"],
        models.PatientReport.reference : dict1.__dict__["reference"],
        models.PatientReport.medicine_id : dict1.__dict__["medicine_id"],
        models.PatientReport.medicine_name : dict1.__dict__["medicine_name"],
        models.PatientReport.doctor_id : dict1.__dict__["doctor_id"],
        models.PatientReport.hospital_id : dict1.__dict__["hospital_id"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Patient Report details updated successfully")

