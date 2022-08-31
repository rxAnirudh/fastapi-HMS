"""Controller file for writing db queries"""
import json
import math
import random
import sys
from fastapi import HTTPException,Request, UploadFile
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Session
from authentication import Authentication
from jwt_utility import JWTUtility
import patient
from patient.email_manager import EmailManager
from response import Response as ResponseData
from patient.app.models import models,schemas
from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.error_handling import Error
import ast
from fastapi.responses import FileResponse

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
  'profile_pic' : f'patient_images/{file}'
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
            data = database.query(models.Allergies).filter(models.Allergies.id == str(allergy.split(",")[i])).first()
            print(f"data {data}")
            if data is None:
                return ResponseData.success_without_data("Allergy id is invalid")
            new_list.append(data)
            allergy_data = {
                "patient_id" : str(db_patient.id),
                "allergy_id" : str(allergy.split(",")[i])
            }
            db_patient_allergies_details = models.Patient_Allergies(**allergy_data)
            database.add(db_patient_allergies_details)
            database.commit()
            database.refresh(db_patient_allergies_details)
        # patient_details_data["allergies"] = new_list
    if len(food_preference.split(",")) > 0 and food_preference != "":
        new_list = []
        for i in range(0,len(str(food_preference).split(","))):
            data = database.query(models.FoodPreference).filter(models.FoodPreference.id == str(food_preference.split(",")[i])).first()
            if data is None:
                return ResponseData.success_without_data("food preference id is invalid")
            new_list.append(data)
            food_preferences = {
                "patient_id" : str(db_patient.id),
                "food_preference_id" : str(food_preference.split(",")[i])
            }
            db_patient_food_preference_details = models.Patient_FoodPreference(**food_preferences)
            database.add(db_patient_food_preference_details)
            database.commit()
            database.refresh(db_patient_food_preference_details)
        # patient_details_data["food_preferences"] = new_list
        new_list = []
    if len(current_medication.split(",")) > 0 and current_medication != "":
        print(f'current_medication.split(",") {current_medication.split(",")}')
        for i in range(0,len(str(current_medication).split(","))):
            if not database.query(models.CurrentMedications).filter(models.CurrentMedications.id == str(current_medication.split(",")[i])).first():
                return ResponseData.success_without_data("Current medication id is invalid")
            new_list.append(database.query(models.CurrentMedications).filter(models.CurrentMedications.id == str(current_medication.split(",")[i])).first())
            current_medications = {
                "patient_id" : str(db_patient.id),
                "current_medication_id" : str(current_medication.split(",")[i])
            }
            db_patient_current_medication_details = models.Patient_CurrentMedications(**current_medications)
            database.add(db_patient_current_medication_details)
            database.commit()
            database.refresh(db_patient_current_medication_details)
        # patient_details_data["current_medications"] = new_list
        new_list = []
    if len(past_injury.split(",")) > 0 and past_injury != "":
        print(f'str(past_injury).split(",") {str(past_injury).split(",")}')
        for i in range(0,len(str(past_injury).split(","))):
            if not database.query(models.PastInjuries).filter(models.PastInjuries.id == str(past_injury.split(",")[i])).first():
                return ResponseData.success_without_data("Past injury id is invalid")
            # new_list.append(database.query(models.PastInjuries).filter(models.PastInjuries.id == str(past_injury.split(",")[i])).first())
            past_injuries = {
                "patient_id" : str(db_patient.id),
                "past_injury_id" : str(past_injury.split(",")[i])
            }
            db_patient_past_injuries_details = models.Patient_PastInjuries(**past_injuries)
            database.add(db_patient_past_injuries_details)
            database.commit()
            database.refresh(db_patient_past_injuries_details)
        # patient_details_data["past_injuries"] = new_list
        new_list = []
    if len(past_surgery.split(",")) > 0 and past_surgery != "":
        for i in range(0,len(str(past_surgery).split(","))):
            if not database.query(models.PastSurgeries).filter(models.PastSurgeries.id == str(past_surgery.split(",")[i])).first():
                return ResponseData.success_without_data("Past surgery id is invalid")
            new_list.append(database.query(models.PastSurgeries).filter(models.PastSurgeries.id == str(past_surgery.split(",")[i])).first())
            past_surgery = {
                "patient_id" : str(db_patient.id),
                "past_surgery_id" : str(past_surgery.split(",")[i])
            }
            db_patient_past_surgeries_details = models.Patient_PastSurgeries(**past_surgery)
            database.add(db_patient_past_surgeries_details)
            database.commit()
            database.refresh(db_patient_past_surgeries_details)
        # patient_details_data["past_surgeries"] = new_list
    if patient_details_data["hospital_id"] is None:
        patient_details_data["hospital_id"] = ""
    # patient_details_data.pop("allergies")
    # patient_details_data.pop("food_preferences")
    # patient_details_data.pop("current_medications")
    # patient_details_data.pop("past_injuries")
    # patient_details_data.pop("past_surgeries")
    return ResponseData.success(patient_details_data,"New Patient added successfully")

def get_patient(request:Request,database: Session, contact_number : str):
    """Function to tell user if patient with given contact number already exists or not"""
    return database.query(models.Patient).filter(models.Patient.contact_number == contact_number).first()

async def patient_forget_password(database: Session, email : Optional[str] = None):
    """Function to tell user if patient with given contact number already exists or not"""
    db_patient_email = database.query(models.Patient).filter(models.Patient.email == email).first()
    if not db_patient_email:
        return ResponseData.success_without_data("Email id is invalid")
    digits = "0123456789"
    OTP = ""
    for i in range(6):
       OTP += digits[math.floor(random.random() * 10)]
    otp = list(OTP)
    if otp[0] == "0":
        otp[0] = "1"
        OTP = "" 
        for i in range(0,len(otp)):
          OTP+=otp[i]
    template = '''
<!DOCTYPE html>
<html>
<body>

<h1>Otp for reseting password</h1>

<p>Your otp is {0}</p>

</body>
</html>
'''.format(OTP)
    print("sdds")
    await EmailManager().forgot_password(
                            email,
                            "Forgot Password",
                            template
                        ),
            # user_otp_data = OtpForPasswordModel.objects.filter(
            #     user_id=user_data.id
            # ).first()
    return database.query(models.Patient).filter(models.Patient.email == email).first()

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
    allergies_list = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(db_patient.id)).all()
    allergies = []
    print(f"allergies_list[i] {allergies_list[0].allergy_id}")
    for i in range(0,len(allergies_list)):
        allergy = database.query(models.Allergies).filter(models.Allergies.id == str(allergies_list[i].allergy_id)).first()
        if allergy is not None:
          allergies.append(allergy)
    db_patient_details.__dict__["patient_allergies"] = allergies
    medications_list = database.query(models.Patient_CurrentMedications).filter(models.Patient_CurrentMedications.patient_id == str(db_patient.id)).all()
    medications = []
    for i in range(0,len(medications_list)):
        medication = database.query(models.CurrentMedications).filter(models.CurrentMedications.id == str(medications_list[i].current_medication_id)).first()
        if medication is not None:
          medications.append(medication)
    db_patient_details.__dict__["patient_current_medications"] = medications
    injuries_list = database.query(models.Patient_PastInjuries).filter(models.Patient_PastInjuries.patient_id == str(db_patient.id)).all()
    injuries = []
    for i in range(0,len(injuries_list)):
        injury = database.query(models.PastInjuries).filter(models.PastInjuries.id == str(injuries_list[i].past_injury_id)).first()
        if injury is not None:
          injuries.append(injury)
    db_patient_details.__dict__["patient_past_injuries"] = injuries
    surgeries_list = database.query(models.Patient_PastSurgeries).filter(models.Patient_PastSurgeries.patient_id == str(db_patient.id)).all()
    surgeries = []
    for i in range(0,len(surgeries_list)):
        surgery = database.query(models.PastSurgeries).filter(models.PastSurgeries.id == str(surgeries_list[i].past_surgery_id)).first()
        if surgery is not None:
          surgeries.append(surgery)
    db_patient_details.__dict__["patient_past_surgeries"] = surgeries
    food_preference_list = database.query(models.Patient_FoodPreference).filter(models.Patient_FoodPreference.patient_id == str(db_patient.id)).all()
    food_preference = []
    for i in range(0,len(food_preference_list)):
        food = database.query(models.FoodPreference).filter(models.FoodPreference.id == str(food_preference_list[i].food_preference_id)).first()
        if food is not None:
          food_preference.append(food)
    db_patient_details.__dict__["patient_food_preferences"] = food_preference
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
    database.query(models.Allergies).filter_by(patient_id = str(id)).delete()
    database.query(models.CurrentMedications).filter_by(patient_id = str(id)).delete()
    database.query(models.PastInjuries).filter_by(patient_id = str(id)).delete()
    database.query(models.PastSurgeries).filter_by(patient_id = str(id)).delete()
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
                      allergy: str, current_medication: str,
                      past_injury: str,past_surgery: str, smoking_habits: str, alchol_consumption: str,
                      activity_level: str, food_preference: str,
                      occupation: str, patient_id: Integer):
    """Function to update patient details"""
    db_patient = database.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        return ResponseData.success({},"Patient with this id does not exists")
    print(f"first_name {db_patient.first_name}")
    dict2 = {
        "first_name": first_name if first_name != "" else db_patient.first_name,
  "last_name": last_name if last_name != "" else db_patient.last_name,
  "contact_number": contact_number if contact_number != "" else db_patient.contact_number,
  "email": email if email != "" else db_patient.email,
  "gender": gender if gender != "" else db_patient.gender,
  "date_of_birth": date_of_birth if date_of_birth != "" else db_patient.date_of_birth,
  "blood_group": blood_group if blood_group != "" else db_patient.blood_group,
  "hospital_id": hospital_id if hospital_id != "" else db_patient.hospital_id,
  'profile_pic' : f"patient_images/{profile_pic}" if profile_pic != "" else f"{db_patient.profile_pic}",
    }
    for key,value in dict2.items():
        update_fields(dict2,key,value)
    db_patient_details = database.query(models.PatientDetails).filter(models.PatientDetails.id == patient_id).first()
    dict1 = {
        "marital_status":marital_status if marital_status != "" else db_patient_details.marital_status,
  "height": height if height != "" else db_patient_details.height,
  "weight": weight if weight != "" else db_patient_details.weight,
  "emergency_contact_number": emergency_contact_number if emergency_contact_number != "" else db_patient_details.emergency_contact_number,
  "city": city if city != "" else db_patient_details.city,
  "smoking_habits" : smoking_habits if smoking_habits != "" else db_patient_details.smoking_habits,
  "alchol_consumption": alchol_consumption if alchol_consumption != "" else db_patient_details.alchol_consumption,
  "activity_level": activity_level if activity_level != "" else db_patient_details.activity_level,
  "occupation" : occupation if occupation != "" else db_patient_details.occupation,
    }
    for key,value in dict1.items():
        update_fields(dict1,key,value)
    if len(allergy.split(",")) > 0 and allergy != "":
        database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(patient_id)).delete()
        for i in range(0,len(str(allergy).split(","))):
            print(f'str(allergy).split(",")[i] {str(allergy).split(",")[i]}')
            # check_if_id_is_valid = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(patient_id),models.Patient_Allergies.allergy_id == str(allergy.split(",")[i])).first()
            # print(f"check_if_id_is_valid {check_if_id_is_valid}")
            # if check_if_id_is_valid is None:
            #     return ResponseData.success_without_data("Allergies id is invalid")
            allergy_data = {
                "patient_id" : str(db_patient.id),
                "allergy_id" : str(allergy.split(",")[i])
            }
            db_patient_allergies_details = models.Patient_Allergies(**allergy_data)
            database.add(db_patient_allergies_details)
            database.commit()
            database.refresh(db_patient_allergies_details)
    if len(current_medication) > 0 :
        database.query(models.Patient_CurrentMedications).filter(models.Patient_CurrentMedications.patient_id == str(patient_id)).delete()
        for i in range(0,len(str(current_medication).split(","))):
            print(f'str(current_medication).split(",")[i] {str(current_medication).split(",")[i]}')
            # check_if_id_is_valid = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(patient_id),models.Patient_Allergies.allergy_id == str(allergy.split(",")[i])).first()
            # print(f"check_if_id_is_valid {check_if_id_is_valid}")
            # if check_if_id_is_valid is None:
            #     return ResponseData.success_without_data("Allergies id is invalid")
            current_medications = {
                "patient_id" : str(db_patient.id),
                "current_medication_id" : str(current_medication.split(",")[i])
            }
            db_patient_current_medication_details = models.Patient_CurrentMedications(**current_medications)
            database.add(db_patient_current_medication_details)
            database.commit()
            database.refresh(db_patient_current_medication_details)
    if len(past_injury) > 0 :
        database.query(models.Patient_PastInjuries).filter(models.Patient_PastInjuries.patient_id == str(patient_id)).delete()
        for i in range(0,len(str(past_injury).split(","))):
            print(f'str(past_injury).split(",")[i] {str(past_injury).split(",")[i]}')
            # check_if_id_is_valid = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(patient_id),models.Patient_Allergies.allergy_id == str(allergy.split(",")[i])).first()
            # print(f"check_if_id_is_valid {check_if_id_is_valid}")
            # if check_if_id_is_valid is None:
            #     return ResponseData.success_without_data("Allergies id is invalid")
            past_injuries = {
                "patient_id" : str(db_patient.id),
                "past_injury_id" : str(past_injury.split(",")[i])
            }
            db_patient_past_injuries_details = models.Patient_PastInjuries(**past_injuries)
            database.add(db_patient_past_injuries_details)
            database.commit()
            database.refresh(db_patient_past_injuries_details)
    if len(past_surgery) > 0 :
        database.query(models.Patient_PastSurgeries).filter(models.Patient_PastSurgeries.patient_id == str(patient_id)).delete()
        for i in range(0,len(str(past_surgery).split(","))):
            print(f'str(past_surgery).split(",")[i] {str(past_surgery).split(",")[i]}')
            # check_if_id_is_valid = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(patient_id),models.Patient_Allergies.allergy_id == str(allergy.split(",")[i])).first()
            # print(f"check_if_id_is_valid {check_if_id_is_valid}")
            # if check_if_id_is_valid is None:
            #     return ResponseData.success_without_data("Allergies id is invalid")
            past_surgery = {
                "patient_id" : str(db_patient.id),
                "past_surgery_id" : str(past_surgery.split(",")[i])
            }
            db_patient_past_surgeries_details = models.Patient_PastSurgeries(**past_surgery)
            database.add(db_patient_past_surgeries_details)
            database.commit()
            database.refresh(db_patient_past_surgeries_details)
    if len(food_preference) > 0 :
        database.query(models.Patient_FoodPreference).filter(models.Patient_FoodPreference.patient_id == str(patient_id)).delete()
        for i in range(0,len(str(food_preference).split(","))):
            print(f'str(food_preference).split(",")[i] {str(food_preference).split(",")[i]}')
            # check_if_id_is_valid = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(patient_id),models.Patient_Allergies.allergy_id == str(allergy.split(",")[i])).first()
            # print(f"check_if_id_is_valid {check_if_id_is_valid}")
            # if check_if_id_is_valid is None:
            #     return ResponseData.success_without_data("Allergies id is invalid")
            food_preferences = {
                "patient_id" : str(db_patient.id),
                "food_preference_id" : str(food_preference.split(",")[i])
            }
            db_patient_food_preference_details = models.Patient_FoodPreference(**food_preferences)
            database.add(db_patient_food_preference_details)
            database.commit()
            database.refresh(db_patient_food_preference_details)
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
        models.PatientDetails.occupation : dict1["occupation"]        
    })
    database.flush()
    database.commit()
    # dict1.update(dict2)
    # allergies_list = database.query(models.Patient_Allergies).filter(models.Patient_Allergies.patient_id == str(db_patient.id)).all()
    # dict1["patient_allergies"] = allergies_list
    # medications_list = database.query(models.Patient_CurrentMedications).filter(models.Patient_CurrentMedications.patient_id == str(db_patient.id)).all()
    # dict1["patient_current_medications"] = medications_list
    # injuries_list = database.query(models.Patient_PastInjuries).filter(models.Patient_PastInjuries.patient_id == str(db_patient.id)).all()
    # dict1["patient_past_injuries"] = injuries_list
    # surgeries_list = database.query(models.Patient_PastSurgeries).filter(models.Patient_PastSurgeries.patient_id == str(db_patient.id)).all()
    # dict1["patient_past_surgeries"] = surgeries_list
    # food_preference_list = database.query(models.Patient_FoodPreference).filter(models.Patient_FoodPreference.patient_id == str(db_patient.id)).all()
    # dict1["patient_food_preference"] = food_preference_list
    return ResponseData.success({},"Patient details updated successfully")


def get_allergies_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    allergies_list = database.query(models.Allergies).filter().all()
    return ResponseData.success(allergies_list,"Allergies details fetched successfully")
    # if id is None:
    #     allergies_list = database.query(models.Allergies).filter().all()
    #     return ResponseData.success(allergies_list,"Allergies details fetched successfully")
    # db_allergy_details = database.query(models.Allergies).filter(models.Allergies.id == id).first()
    # if db_allergy_details is None:
    #     return ResponseData.success_without_data("Id is invalid or allergies does not exists")
    # return ResponseData.success(db_allergy_details.__dict__,"Allergies details fetched successfully")

def add_allergy(database: Session,allergy_name):
    """Function to add allergy"""
    if allergy_name is None:
        return ResponseData.success_without_data("Please provide allergy name")
    db_allergy_details = database.query(models.Allergies).filter(models.Allergies.allergy == allergy_name).first()
    if db_allergy_details:
        return ResponseData.success_without_data("Allergy with this name already exists")
    data = {
        "allergy" : allergy_name
    }
    db_allergy_details = models.Allergies(**data)
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
    db_current_medication_details = database.query(models.CurrentMedications).filter(models.CurrentMedications.current_medication == current_medication_name).first()
    if db_current_medication_details:
        return ResponseData.success_without_data("Current medication with this name already exists")
    data = {
        "current_medication" : current_medication_name
    }
    db_current_medication_details = models.CurrentMedications(**data)
    database.add(db_current_medication_details)
    database.commit()
    database.refresh(db_current_medication_details)
    return ResponseData.success(db_current_medication_details.__dict__,"Current medication added successfully")

def add_past_injury(database: Session,injury_name):
    """Function to add past injury"""
    if injury_name is None:
        return ResponseData.success_without_data("Please provide past injury name")
    db_injury_details = database.query(models.PastInjuries).filter(models.PastInjuries.past_injury == injury_name).first()
    if db_injury_details:
        return ResponseData.success_without_data("Injury with this name already exists")
    data = {
        "past_injury" : injury_name
    }
    db_past_injury_details = models.PastInjuries(**data)
    database.add(db_past_injury_details)
    database.commit()
    database.refresh(db_past_injury_details)
    return ResponseData.success(db_past_injury_details.__dict__,"Past injuries added successfully")

def add_past_surgery(database: Session,surgery_name):
    """Function to add past surgery"""
    if surgery_name is None:
        return ResponseData.success_without_data("Please provide past surgery name")
    db_allergy_details = database.query(models.PastSurgeries).filter(models.PastSurgeries.past_surgery == surgery_name).first()
    if db_allergy_details:
        return ResponseData.success_without_data("Surgery with this name already exists")
    data = {
        "past_surgery" : surgery_name
    }
    db_past_surgery_details = models.PastSurgeries(**data)
    database.add(db_past_surgery_details)
    database.commit()
    database.refresh(db_past_surgery_details)
    return ResponseData.success(db_past_surgery_details.__dict__,"Past surgeries added successfully")

def get_current_medication_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    current_medications_list = database.query(models.CurrentMedications).filter().all()
    return ResponseData.success(current_medications_list,"Patient current medications details fetched successfully")

def get_food_preferences(database: Session):
    """Function to get_food_preferences"""
    food_preferences = database.query(models.FoodPreference).filter().all()
    return ResponseData.success(food_preferences,"Food preference details fetched successfully")
    # if id is None:
    #     current_medications_list = database.query(models.CurrentMedications).filter().all()
    #     return ResponseData.success(current_medications_list,"Patient current medications details fetched successfully")
    # db_current_medications_details = database.query(models.CurrentMedications).filter(models.CurrentMedications.id == id).first()
    # if db_current_medications_details is None:
    #     return ResponseData.success_without_data("Id is invalid or current medications does not exists")
    # return ResponseData.success(db_current_medications_details.__dict__,"Current medications details fetched successfully")

def get_past_injuries_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    past_injuries_list = database.query(models.PastInjuries).filter().all()
    return ResponseData.success(past_injuries_list,"Past injuries details fetched successfully")
    # if id is None:
    #     past_injuries_list = database.query(models.PastInjuries).filter().all()
    #     return ResponseData.success(past_injuries_list,"Past injuries details fetched successfully")
    # db_past_injuries_details = database.query(models.PastInjuries).filter(models.PastInjuries.id == id).first()
    # if db_past_injuries_details is None:
    #     return ResponseData.success_without_data("Id is invalid or past injuries does not exists")
    # return ResponseData.success(db_past_injuries_details.__dict__,"Past injuries details fetched successfully")

def get_past_surgeries_by_id(database: Session):
    """Function to tell user if patient with given contact number already exists or not"""
    past_surgeries_list = database.query(models.PastSurgeries).filter().all()
    return ResponseData.success(past_surgeries_list,"Patient past surgeries details fetched successfully")
    # if id is None:
    #     past_surgeries_list = database.query(models.PastSurgeries).filter().all()
    #     return ResponseData.success(past_surgeries_list,"Patient past surgeries details fetched successfully")
    # db_past_surgeries_details = database.query(models.PastSurgeries).filter(models.PastSurgeries.id == id).first()
    # if db_past_surgeries_details is None:
    #     return ResponseData.success_without_data("Id is invalid or past surgeries does not exists")
    # return ResponseData.success(db_past_surgeries_details.__dict__,"Past surgeries details fetched successfully")