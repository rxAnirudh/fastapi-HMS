"""Controller file for writing db queries"""
import json
import sys
from fastapi import HTTPException,Request, UploadFile
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Session
from authentication import Authentication
from jwt_utility import JWTUtility
import patient
from response import Response as ResponseData
from patient.app.models import models,schemas
from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.error_handling import Error
import ast
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_patient(database: Session, file: UploadFile, first_name: str, last_name: str, contact_number: str,password: str,
                      email: str, gender: str,
                      date_of_birth: str, blood_group: str,
                      hospital_id: str,marital_status: str, height: str, weight: str,
                      emergency_contact_number: str, city: str,
                      allergy: str, current_medication: str,
                      past_injury: str,past_surgery: str, smoking_habits: str, alchol_consumption: str,
                      activity_level: str, food_preference: str,
                      occupation: str):
    """Function to add new patient data"""
    db_patient_email = database.query(models.Patient).filter(models.Patient.email == email).first()
    db_patient_number = database.query(models.Patient).filter(models.Patient.contact_number == contact_number).first()
    if db_patient_email or db_patient_number:
        return ResponseData.success_without_data("This user already exists")
    patientdata = {
        "first_name": first_name,
  "last_name": last_name,
  "contact_number": contact_number,
  "password" : password,
  "email": email,
  "gender": gender,
  "date_of_birth": date_of_birth,
  "blood_group": blood_group,
  "hospital_id": hospital_id,
  'profile_pic' : file
    }
    db_patient = models.Patient(**patientdata)
    database.add(db_patient)
    database.commit()
    database.refresh(db_patient)
    patient_details_data = {
        "id" : db_patient.id,
        "marital_status": marital_status,
  "height": height,
  "weight": weight,
  "emergency_contact_number": emergency_contact_number,
  "city": city,
  "smoking_habits" : smoking_habits,
  "alchol_consumption": alchol_consumption,
  "activity_level": activity_level,
  "occupation" : occupation,
    }
    db_patient_details = models.PatientDetails(**patient_details_data)
    database.add(db_patient_details)
    database.commit()
    database.refresh(db_patient_details)
    Merge(patientdata, patient_details_data)
    token = {
        'authentication_token' : JWTUtility.encode_token(db_patient.email,db_patient.contact_number)
    }
    Merge(token, patient_details_data)
    if len(allergy.split(",")) > 0 and allergy != "":
        new_list = []
        for i in range(0,len(str(allergy).split(","))):
            data = database.query(models.PatientAllergies).filter(models.PatientAllergies.id == str(allergy.split(",")[i])).first()
            print(f"data {data}")
            if data is None:
                return ResponseData.success_without_data("Allergy id is invalid")
            new_list.append(data)
        patient_details_data["allergies"] = new_list
    if len(food_preference.split(",")) > 0 and food_preference != "":
        new_list = []
        for i in range(0,len(str(food_preference).split(","))):
            data = database.query(models.FoodPreference).filter(models.FoodPreference.id == str(food_preference.split(",")[i])).first()
            if data is None:
                return ResponseData.success_without_data("food preference id is invalid")
            new_list.append(data)
        patient_details_data["food_preferences"] = new_list
        new_list = []
    if len(current_medication.split(",")) > 0 and current_medication != "":
        for i in range(0,len(str(current_medication).split(","))):
            if not database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.id == str(current_medication.split(",")[i])).first():
                return ResponseData.success_without_data("Current medication id is invalid")
            new_list.append(database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.id == str(current_medication.split(",")[i])).first())
        patient_details_data["current_medications"] = new_list
        new_list = []
    if len(past_injury.split(",")) > 0 and past_injury != "":
        for i in range(0,len(str(past_injury).split(","))):
            if not database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.id == str(past_injury.split(",")[i])).first():
                return ResponseData.success_without_data("Past injury id is invalid")
            new_list.append(database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.id == str(past_injury.split(",")[i])).first())
        patient_details_data["past_injuries"] = new_list
        new_list = []
    if len(past_surgery.split(",")) > 0 and past_surgery != "":
        for i in range(0,len(str(past_surgery).split(","))):
            if not database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.id == str(past_surgery.split(",")[i])).first():
                return ResponseData.success_without_data("Past surgery id is invalid")
            new_list.append(database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.id == str(past_surgery.split(",")[i])).first())
        patient_details_data["past_surgeries"] = new_list
    if patient_details_data["hospital_id"] is None:
        patient_details_data["hospital_id"] = ""
    patient_details_data.pop("password")
    return ResponseData.success(patient_details_data,"New Patient added successfully")

def get_patient(request:Request,database: Session, contact_number : str):
    """Function to tell user if patient with given contact number already exists or not"""
    return database.query(models.Patient).filter(models.Patient.contact_number == contact_number).first()

def reset_password_for_patient(database: Session, old_password : str,new_password : str,patient_id:int):
    """Function to reset password for a particular patient"""
    db_patient = database.query(models.Patient).filter(models.Patient.id == patient_id,models.Patient.password == old_password).first()
    if not db_patient:
        return ResponseData.success_without_data("Password is invalid")
    database.query(models.Patient).filter(models.Patient.id == patient_id).update({
        models.Patient.password : new_password,     
    })
    database.flush()
    database.commit()
    return ResponseData.success({},"Password has been updated successfully")

def patient_sign_in_api(database: Session,email : Optional[str] = None,password : Optional[str] = None):
    """Function to sign in a patient"""
    db_patient = database.query(models.Patient).filter(models.Patient.email == email,models.Patient.password == password).first()
    if not db_patient:
        return ResponseData.success_without_data("Credentials are invalid")
    db_patient_details = database.query(models.Patient).filter(models.Patient.email == email).first()
    token = {
        'authentication_token' : JWTUtility.encode_token(db_patient_details.email,db_patient_details.contact_number)
    }
    Merge(token, db_patient_details.__dict__)
    if db_patient_details.__dict__["hospital_id"] is None:
        db_patient_details.__dict__["hospital_id"] = ""
    db_patient_details.__dict__.pop("password")
    return ResponseData.success(db_patient_details.__dict__,"Patient signed in successfully")

def get_patient_by_id(database: Session, id : Optional[int] = None):
    """Function to tell user if patient with given contact number already exists or not"""
    if id is None:
        db_patient = database.query(models.Patient).filter().first()
        db_patient_details = database.query(models.PatientDetails).filter().first()
        Merge(db_patient.__dict__, db_patient_details.__dict__)
        return ResponseData.success(db_patient_details.__dict__,"Patient details fetched successfully")
    db_patient = database.query(models.Patient).filter(models.Patient.id == id).first()
    if db_patient is None:
        return ResponseData.success([],"Patient with this id does not exists")
    db_patient_details = database.query(models.PatientDetails).filter(models.PatientDetails.id == id).first()
    Merge(db_patient.__dict__, db_patient_details.__dict__)
    allergies_list = database.query(models.PatientAllergies).filter(models.PatientAllergies.patient_id == str(db_patient.id)).all()
    db_patient_details.__dict__["allergies"] = allergies_list
    medications_list = database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.patient_id == str(db_patient.id)).all()
    db_patient_details.__dict__["current_medications"] = medications_list
    injuries_list = database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.patient_id == str(db_patient.id)).all()
    db_patient_details.__dict__["past_injuries"] = injuries_list
    surgeries_list = database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.patient_id == str(db_patient.id)).all()
    db_patient_details.__dict__["past_surgeries"] = surgeries_list
    if db_patient_details.__dict__["hospital_id"] is None:
        db_patient_details.__dict__["hospital_id"] = ""
    return ResponseData.success(db_patient_details.__dict__,"Patient details fetched successfully")

def get_patient_by_pagination(database: Session,page : int,size:int):
    """Function to get patient details by pagination"""
    data = database.query(models.Patient,models.PatientDetails).filter(models.Patient.id == models.PatientDetails.id).all()
    listdata = []
    if(len(data) > 1):
         for i, ele in enumerate(data):
            dict1 = ele["PatientDetails"]
            dict2 = ele["Patient"]
            dict1.__dict__.update(dict2.__dict__)
            listdata.append(dict1)      
         data = listdata[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Patient details fetched successfully")
         return ResponseData.success([],"No Patient found")  
    return ResponseData.success(listdata,"No Patient found")

def delete_patient_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all patient details if needed"""
    if id is None:
        database.query(models.Patient).delete()
        database.commit()
        return ResponseData.success([],"All Patient details deleted successfully")
    database.query(models.Patient).filter_by(id = id).delete()
    database.query(models.PatientDetails).filter_by(id = id).delete()
    database.query(models.PatientAllergies).filter_by(patient_id = str(id)).delete()
    database.query(models.PatientCurrentMedications).filter_by(patient_id = str(id)).delete()
    database.query(models.PatientPastInjuries).filter_by(patient_id = str(id)).delete()
    database.query(models.PatientPastSurgeries).filter_by(patient_id = str(id)).delete()
    database.commit()
    return ResponseData.success([],"Patient details deleted successfully")

def check_if_patient_id_is_valid(database: Session, id : Optional[int] = None):
    """Function to check if patient id exists or not"""
    hospital_data = database.query(models.Patient).filter(models.Patient.id == id).first()
    if hospital_data:
        return True
    else:
        return False

def update_fields(actualDict,key,value):
    if key != '' or key is not None:
        actualDict[f"{key}"] = value

def update_patient_details(database: Session, profile_pic: UploadFile, first_name: str, last_name: str, contact_number: str,
                      email: str, gender: str,
                      date_of_birth: str, blood_group: str,
                      hospital_id: str,marital_status: str, height: str, weight: str,
                      emergency_contact_number: str, city: str,
                      allergy: list, current_medication: str,
                      past_injury: str,past_surgery: str, smoking_habits: str, alchol_consumption: str,
                      activity_level: str, food_preference: str,
                      occupation: str,patient_id: Integer):
    """Function to update patient details"""
    db_patient = database.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        return ResponseData.success({},"Patient with this id does not exists")
    dict2 = {
        "first_name": first_name,
  "last_name": last_name,
  "contact_number": contact_number,
  "email": email,
  "gender": gender,
  "date_of_birth": date_of_birth,
  "blood_group": blood_group,
  "hospital_id": hospital_id,
  'profile_pic' : profile_pic
    }
    for key,value in dict2.items():
        update_fields(dict2,key,value)
    dict1 = {
        "marital_status": marital_status,
  "height": height,
  "weight": weight,
  "emergency_contact_number": emergency_contact_number,
  "city": city,
  "smoking_habits" : smoking_habits,
  "alchol_consumption": alchol_consumption,
  "activity_level": activity_level,
  'food_preference' : food_preference,
  "occupation" : occupation
    }
    for key,value in dict1.items():
        update_fields(dict1,key,value)
    if len(allergy) > 0 :
        final_list = json.loads(allergy[0])
        for i in range(0,len(final_list)):
            check_if_id_is_valid = database.query(models.PatientAllergies).filter(patient_id == patient_id,models.PatientAllergies.id == int(final_list[i]["id"])).first()
            if check_if_id_is_valid is None:
                return ResponseData.success_without_data("Allergies id is invalid")
            database.query(models.PatientAllergies).filter(models.PatientAllergies.id == int(final_list[i]["id"])).update({ 
        models.PatientAllergies.allergy : final_list[i]["allergy"],
        models.PatientAllergies.id : int(final_list[i]["id"])
    })
    if len(current_medication) > 0 :
        final_list = json.loads(current_medication[0])
        for i in range(0,len(final_list)):
            check_if_id_is_valid = database.query(models.PatientCurrentMedications).filter(patient_id == patient_id,models.PatientCurrentMedications.id == int(final_list[i]["id"])).first()
            if check_if_id_is_valid is None:
                return ResponseData.success_without_data("Current Medications id is invalid")
            database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.id == int(final_list[i]["id"])).update({ 
        models.PatientCurrentMedications.current_medication : final_list[i]["current_medication"],
        models.PatientCurrentMedications.id : int(final_list[i]["id"])
    })
    if len(past_injury) > 0 :
        final_list = json.loads(past_injury[0])
        for i in range(0,len(final_list)):
            check_if_id_is_valid = database.query(models.PatientPastInjuries).filter(patient_id == patient_id,models.PatientPastInjuries.id == int(final_list[i]["id"])).first()
            if check_if_id_is_valid is None:
                return ResponseData.success_without_data("Past Injury id is invalid")
            database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.id == int(final_list[i]["id"])).update({ 
        models.PatientPastInjuries.past_injury : final_list[i]["past_injury"],
        models.PatientPastInjuries.id : int(final_list[i]["id"])
    })
    if len(past_surgery) > 0 :
        final_list = json.loads(past_surgery[0])
        for i in range(0,len(final_list)):
            check_if_id_is_valid = database.query(models.PatientPastSurgeries).filter(patient_id == patient_id,models.PatientPastSurgeries.id == int(final_list[i]["id"])).first()
            if check_if_id_is_valid is None:
                return ResponseData.success_without_data("Past surgery id is invalid")
            database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.id == int(final_list[i]["id"])).update({ 
        models.PatientPastSurgeries.past_surgery : final_list[i]["past_surgery"],
        models.PatientPastSurgeries.id : int(final_list[i]["id"])
    })
    database.query(models.Patient).filter(models.Patient.id == patient_id).update({ models.Patient.id : patient_id,
        models.Patient.first_name: dict2["first_name"],
        models.Patient.last_name : dict2["last_name"],
        models.Patient.contact_number : dict2["contact_number"],
        models.Patient.profile_pic : dict2["profile_pic"],
        models.Patient.email : dict2["email"],
        models.Patient.gender : dict2["gender"],
        models.Patient.date_of_birth : dict2["date_of_birth"],
        models.Patient.blood_group : dict2["blood_group"],
        # models.Patient.hospital_id : dict2["hospital_id"],
    })
    database.query(models.PatientDetails).filter(models.PatientDetails.id == patient_id).update({
        models.PatientDetails.id : patient_id,
        models.PatientDetails.marital_status : dict1["marital_status"],
        models.PatientDetails.height : dict1["height"],
        models.PatientDetails.weight : dict1["weight"],
        models.PatientDetails.emergency_contact_number : dict1["emergency_contact_number"],
        models.PatientDetails.city : dict1["city"],
        models.PatientDetails.smoking_habits : dict1["smoking_habits"],
        models.PatientDetails.alchol_consumption : dict1["alchol_consumption"],
        models.PatientDetails.activity_level : dict1["activity_level"],
        models.PatientDetails.food_preference : dict1["food_preference"],
        models.PatientDetails.occupation : dict1["occupation"]        
    })
    database.flush()
    database.commit()
    dict1.update(dict2)
    allergies_list = database.query(models.PatientAllergies).filter(models.PatientAllergies.patient_id == str(db_patient.id)).all()
    dict1["allergies"] = allergies_list
    medications_list = database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.patient_id == str(db_patient.id)).all()
    dict1["current_medications"] = medications_list
    injuries_list = database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.patient_id == str(db_patient.id)).all()
    dict1["past_injuries"] = injuries_list
    surgeries_list = database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.patient_id == str(db_patient.id)).all()
    dict1["past_surgeries"] = surgeries_list
    return ResponseData.success(dict1,"Patient details updated successfully")


def get_allergies_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    allergies_list = database.query(models.PatientAllergies).filter().all()
    return ResponseData.success(allergies_list,"Allergies details fetched successfully")
    # if id is None:
    #     allergies_list = database.query(models.PatientAllergies).filter().all()
    #     return ResponseData.success(allergies_list,"Allergies details fetched successfully")
    # db_allergy_details = database.query(models.PatientAllergies).filter(models.PatientAllergies.id == id).first()
    # if db_allergy_details is None:
    #     return ResponseData.success_without_data("Id is invalid or allergies does not exists")
    # return ResponseData.success(db_allergy_details.__dict__,"Allergies details fetched successfully")

def add_allergy(database: Session,allergy_name):
    """Function to add allergy"""
    if allergy_name is None:
        return ResponseData.success_without_data("Please provide allergy name")
    db_allergy_details = database.query(models.PatientAllergies).filter(models.PatientAllergies.allergy == allergy_name).first()
    if db_allergy_details:
        return ResponseData.success_without_data("Allergy with this name already exists")
    data = {
        "allergy" : allergy_name
    }
    db_allergy_details = models.PatientAllergies(**data)
    database.add(db_allergy_details)
    database.commit()
    database.refresh(db_allergy_details)
    return ResponseData.success(db_allergy_details.__dict__,"Allergy added successfully")

def add_food_preference(database: Session,food_preference_name):
    """Function to add food preferences"""
    if food_preference_name is None:
        return ResponseData.success_without_data("Please provide food preference name")
    db_food_preference_details = database.query(models.FoodPreference).filter(models.FoodPreference.food_preference == food_preference_name).first()
    if db_food_preference_details:
        return ResponseData.success_without_data("Allergy with this name already exists")
    data = {
        "food_preference" : food_preference_name
    }
    db_food_preference = models.FoodPreference(**data)
    database.add(db_food_preference)
    database.commit()
    database.refresh(db_food_preference)
    return ResponseData.success(db_food_preference.__dict__,"Food preference added successfully")

def add_current_medication(database: Session,current_medication_name):
    """Function to add current medication"""
    if current_medication_name is None:
        return ResponseData.success_without_data("Please provide current medication name")
    db_current_medication_details = database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.current_medication == current_medication_name).first()
    if db_current_medication_details:
        return ResponseData.success_without_data("Current medication with this name already exists")
    data = {
        "current_medication" : current_medication_name
    }
    db_current_medication_details = models.PatientCurrentMedications(**data)
    database.add(db_current_medication_details)
    database.commit()
    database.refresh(db_current_medication_details)
    return ResponseData.success(db_current_medication_details.__dict__,"Current medication added successfully")

def add_past_injury(database: Session,injury_name):
    """Function to add past injury"""
    if injury_name is None:
        return ResponseData.success_without_data("Please provide past injury name")
    db_injury_details = database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.past_injury == injury_name).first()
    if db_injury_details:
        return ResponseData.success_without_data("Injury with this name already exists")
    data = {
        "past_injury" : injury_name
    }
    db_past_injury_details = models.PatientPastInjuries(**data)
    database.add(db_past_injury_details)
    database.commit()
    database.refresh(db_past_injury_details)
    return ResponseData.success(db_past_injury_details.__dict__,"Past injuries added successfully")

def add_past_surgery(database: Session,surgery_name):
    """Function to add past surgery"""
    if surgery_name is None:
        return ResponseData.success_without_data("Please provide past surgery name")
    db_allergy_details = database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.past_surgery == surgery_name).first()
    if db_allergy_details:
        return ResponseData.success_without_data("Surgery with this name already exists")
    data = {
        "past_surgery" : surgery_name
    }
    db_past_surgery_details = models.PatientPastSurgeries(**data)
    database.add(db_past_surgery_details)
    database.commit()
    database.refresh(db_past_surgery_details)
    return ResponseData.success(db_past_surgery_details.__dict__,"Past surgeries added successfully")

def get_current_medication_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    current_medications_list = database.query(models.PatientCurrentMedications).filter().all()
    return ResponseData.success(current_medications_list,"Patient current medications details fetched successfully")

def get_food_preferences(database: Session):
    """Function to get_food_preferences"""
    food_preferences = database.query(models.FoodPreference).filter().all()
    return ResponseData.success(food_preferences,"Food preference details fetched successfully")
    # if id is None:
    #     current_medications_list = database.query(models.PatientCurrentMedications).filter().all()
    #     return ResponseData.success(current_medications_list,"Patient current medications details fetched successfully")
    # db_current_medications_details = database.query(models.PatientCurrentMedications).filter(models.PatientCurrentMedications.id == id).first()
    # if db_current_medications_details is None:
    #     return ResponseData.success_without_data("Id is invalid or current medications does not exists")
    # return ResponseData.success(db_current_medications_details.__dict__,"Current medications details fetched successfully")

def get_past_injuries_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    past_injuries_list = database.query(models.PatientPastInjuries).filter().all()
    return ResponseData.success(past_injuries_list,"Past injuries details fetched successfully")
    # if id is None:
    #     past_injuries_list = database.query(models.PatientPastInjuries).filter().all()
    #     return ResponseData.success(past_injuries_list,"Past injuries details fetched successfully")
    # db_past_injuries_details = database.query(models.PatientPastInjuries).filter(models.PatientPastInjuries.id == id).first()
    # if db_past_injuries_details is None:
    #     return ResponseData.success_without_data("Id is invalid or past injuries does not exists")
    # return ResponseData.success(db_past_injuries_details.__dict__,"Past injuries details fetched successfully")

def get_past_surgeries_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    past_surgeries_list = database.query(models.PatientPastSurgeries).filter().all()
    return ResponseData.success(past_surgeries_list,"Patient past surgeries details fetched successfully")
    # if id is None:
    #     past_surgeries_list = database.query(models.PatientPastSurgeries).filter().all()
    #     return ResponseData.success(past_surgeries_list,"Patient past surgeries details fetched successfully")
    # db_past_surgeries_details = database.query(models.PatientPastSurgeries).filter(models.PatientPastSurgeries.id == id).first()
    # if db_past_surgeries_details is None:
    #     return ResponseData.success_without_data("Id is invalid or past surgeries does not exists")
    # return ResponseData.success(db_past_surgeries_details.__dict__,"Past surgeries details fetched successfully")