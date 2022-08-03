import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from patient.app.models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_patient(database: Session, patient: schemas.PatientBase):
    """Function to return query based data while creating new patient creation api"""
    if not check_if_hospital_id_is_valid(database,patient.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    patient_dict = {'first_name': patient.dict()["first_name"], 'last_name': patient.dict()["last_name"],"contact_number" : patient.dict()["contact_number"],
    "profile_pic" : patient.dict()["profile_pic"],"email" : patient.dict()["email"],"gender" : patient.dict()["gender"],"date_of_birth" : patient.dict()["date_of_birth"],
    "blood_group" : patient.dict()["blood_group"],"hospital_id" : patient.dict()["hospital_id"]}
    db_patient = models.Patient(**patient_dict)
    database.add(db_patient)
    database.commit()
    database.refresh(db_patient)
    patient_details_dict = {'marital_status': patient.dict()["marital_status"],"height" : patient.dict()["height"],
    "weight" : patient.dict()["weight"],"emergency_contact_number" : patient.dict()["emergency_contact_number"],"city" : patient.dict()["city"],
    "allergies" : patient.dict()["allergies"],"current_medications" : patient.dict()["current_medications"],"past_injuries" : patient.dict()["past_injuries"],
    "past_surgeries" : patient.dict()["past_surgeries"],"smoking_habits" : patient.dict()["smoking_habits"],
    "alchol_consumption" : patient.dict()["alchol_consumption"],"activity_level" : patient.dict()["activity_level"],
    "food_preference" : patient.dict()["food_preference"],"occupation" : patient.dict()["occupation"],"id" : db_patient.id,}
    db_patient_details = models.PatientDetails(**patient_details_dict)
    database.add(db_patient_details)
    database.commit()
    database.refresh(db_patient_details)
    Merge(patient_dict, patient_details_dict)
    return ResponseData.success(patient_details_dict,"Patient added successfully")

def get_patient(database: Session, contact_number : str):
    """Function to tell user if patient with given contact number already exists or not"""
    return database.query(models.Patient).filter(models.Patient.contact_number == contact_number).first()

def get_patient_by_id(database: Session, id : Optional[int] = None):
    """Function to tell user if patient with given contact number already exists or not"""
    db_patient = database.query(models.Patient).filter(models.Patient.id == id).first()
    if db_patient is None:
        return ResponseData.success([],"Patient with this id does not exists")
    db_patient_details = database.query(models.PatientDetails).filter(models.PatientDetails.id == id).first()
    Merge(db_patient.__dict__, db_patient_details.__dict__)
    return ResponseData.success(db_patient_details.__dict__,"Patient details fetched successfully")

def delete_patient_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all patient details if needed"""
    if id is None:
        database.query(models.Patient).delete()
        database.commit()
        return ResponseData.success([],"All Patient details deleted successfully")
    database.query(models.Patient).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Patient details deleted successfully")

def check_if_patient_id_is_valid(database: Session, id : Optional[int] = None):
    hospital_data = database.query(models.Patient).filter(models.Patient.id == id).first()
    if hospital_data:
        return True
    else:
        return False

def update_patient_details(database: Session, patient: schemas.AddNewPatient):
    """Function to return query based data while creating add_new_staff creation api"""
    data = database.query(models.PatientDetails,models.Patient).filter(models.Patient.id == patient.id).all()
    dict1 = data[0]["PatientDetails"]
    dict2 = data[0]["Patient"]
    if patient.dict()["first_name"] is not None :
        dict2.__dict__["first_name"] = patient.dict()["first_name"]
    if patient.dict()["last_name"] is not None :
        dict2.__dict__["last_name"] = patient.dict()["last_name"]
    if patient.dict()["contact_number"] is not None :
        dict2.__dict__["contact_number"] = patient.dict()["contact_number"]
    if patient.dict()["profile_pic"] is not None :
        dict2.__dict__["profile_pic"] = patient.dict()["profile_pic"]
    if patient.dict()["email"] is not None :
        dict2.__dict__["email"] = patient.dict()["email"]
    if patient.dict()["gender"] is not None :
        dict2.__dict__["gender"] = patient.dict()["gender"]
    if patient.dict()["date_of_birth"] is not None :
        dict2.__dict__["date_of_birth"] = patient.dict()["date_of_birth"]
    if patient.dict()["blood_group"] is not None :
        dict2.__dict__["blood_group"] = patient.dict()["blood_group"]
    if patient.dict()["hospital_id"] is not None :
        dict2.__dict__["hospital_id"] = patient.dict()["hospital_id"]
    if patient.dict()["marital_status"] is not None :
        dict1.__dict__["marital_status"] = patient.dict()["marital_status"]
    if patient.dict()["height"] is not None :
        dict1.__dict__["height"] = patient.dict()["height"]
    if patient.dict()["weight"] is not None :
        dict1.__dict__["weight"] = patient.dict()["weight"]
    if patient.dict()["emergency_contact_number"] is not None :
        dict1.__dict__["emergency_contact_number"] = patient.dict()["emergency_contact_number"]
    if patient.dict()["city"] is not None :
        dict1.__dict__["city"] = patient.dict()["city"]
    if patient.dict()["allergies"] is not None :
        dict1.__dict__["allergies"] = patient.dict()["allergies"]
    if patient.dict()["current_medications"] is not None :
        dict1.__dict__["current_medications"] = patient.dict()["current_medications"]
    if patient.dict()["past_injuries"] is not None :
        dict1.__dict__["past_injuries"] = patient.dict()["past_injuries"]
    if patient.dict()["past_surgeries"] is not None :
        dict1.__dict__["past_surgeries"] = patient.dict()["past_surgeries"]
    if patient.dict()["smoking_habits"] is not None :
        dict1.__dict__["smoking_habits"] = patient.dict()["smoking_habits"]
    if patient.dict()["alchol_consumption"] is not None :
        dict1.__dict__["alchol_consumption"] = patient.dict()["alchol_consumption"]
    if patient.dict()["activity_level"] is not None :
        dict1.__dict__["activity_level"] = patient.dict()["activity_level"]
    if patient.dict()["food_preference"] is not None :
        dict1.__dict__["food_preference"] = patient.dict()["food_preference"]
    if patient.dict()["occupation"] is not None :
        dict1.__dict__["occupation"] = patient.dict()["occupation"]
    database.query(models.Patient).filter(models.Patient.id == patient.id).update({ models.Patient.id : patient.id,
        models.Patient.first_name: dict2.__dict__["first_name"],
        models.Patient.last_name : dict2.__dict__["last_name"],
        models.Patient.contact_number : dict2.__dict__["contact_number"],
        models.Patient.profile_pic : dict2.__dict__["profile_pic"],
        models.Patient.email : dict2.__dict__["email"],
        models.Patient.gender : dict2.__dict__["gender"],
        models.Patient.date_of_birth : dict2.__dict__["date_of_birth"],
        models.Patient.blood_group : dict2.__dict__["blood_group"],
        models.Patient.hospital_id : dict2.__dict__["hospital_id"],
    })
    database.query(models.PatientDetails).filter(models.PatientDetails.id == patient.id).update({
        models.PatientDetails.id : patient.id,
        models.PatientDetails.marital_status : dict1.__dict__["marital_status"],
        models.PatientDetails.height : dict1.__dict__["height"],
        models.PatientDetails.weight : dict1.__dict__["weight"],
        models.PatientDetails.emergency_contact_number : dict1.__dict__["emergency_contact_number"],
        models.PatientDetails.city : dict1.__dict__["city"],
        models.PatientDetails.allergies : dict1.__dict__["allergies"],
        models.PatientDetails.current_medications : dict1.__dict__["current_medications"],
        models.PatientDetails.past_injuries : dict1.__dict__["past_injuries"],
        models.PatientDetails.past_surgeries : dict1.__dict__["past_surgeries"],
        models.PatientDetails.smoking_habits : dict1.__dict__["smoking_habits"],
        models.PatientDetails.alchol_consumption : dict1.__dict__["alchol_consumption"],
        models.PatientDetails.activity_level : dict1.__dict__["activity_level"],
        models.PatientDetails.food_preference : dict1.__dict__["food_preference"],
        models.PatientDetails.occupation : dict1.__dict__["occupation"],        
    })
    database.flush()
    database.commit()
    dict1.__dict__.update(dict2.__dict__)
    return ResponseData.success(dict1.__dict__,"Patient details updated successfully")
