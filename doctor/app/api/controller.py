"""Controller file for writing db queries"""
from datetime import datetime
import math
import random
from typing import Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy import Integer
from sqlalchemy.orm import Session
from doctor.app.error_handling import Error
from doctor.app.response import Response as ResponseData
from doctor.app.models import models
from jwt_utility import JWTUtility
from patient.app.models import models as patientModels
from patient.email_manager import EmailManager
# from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.api.controller import check_if_patient_id_is_valid
# from staff.app.api.controller import check_if_staff_id_is_valid

# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge"""
    return dict2.update(dict1)

def check_if_doctor_id_is_valid(database: Session, id : Optional[int] = None):
    """Function to check if doctor id is valid or not"""
    doctor_data = database.query(models.Doctor).filter(models.Doctor.id == id).first()
    if doctor_data:
        return True
    else:
        return False

def add_new_doctor(database: Session,file: UploadFile, first_name: str, last_name: str, contact_number: str,
                      email: str,password:str, gender: str,
                      date_of_birth: str, blood_group: str,
                      years_of_experience: str,next_available_at: str, specialist_field: str, education: str,about : str,hospital_id:str,
                      in_clinic_appointment_fees: str,rating:str):
    """Function to add new doctor data"""
    # db_doctor_email = database.query(models.Doctor).filter(models.Doctor.email == email).first()
    # db_doctor_number = database.query(models.Doctor).filter(models.Doctor.contact_number == contact_number).first()
    # if db_doctor_email or db_doctor_number:
    #     return ResponseData.success_without_data("This doctor already exists")
    doctordata = {
        "first_name": first_name,
  "last_name": last_name,
  "contact_number": contact_number,
  "profile_pic" : f'doctor/app/doctor_images/{file}' if file != "" else "",
  "email": email,
  "password" : password,
  "gender": gender,
  "date_of_birth": date_of_birth,
  "blood_group": blood_group,
  "hospital_id" : hospital_id
    }
    db_doctor = models.Doctor(**doctordata)
    database.add(db_doctor)
    database.commit()
    database.refresh(db_doctor)
    doctor_details_data = {
        "id" : db_doctor.id,
        "years_of_experience": years_of_experience,
  "next_available_at": next_available_at,
  "specialist_field": specialist_field,
  "education": education,
  "about": about,
  "in_clinic_appointment_fees": in_clinic_appointment_fees,
  "create_at" : "",
    }
    db_doctor_details = models.DoctorDetails(**doctor_details_data)
    database.add(db_doctor_details)
    database.commit()
    database.refresh(db_doctor_details)
    Merge(doctordata, doctor_details_data)
    return ResponseData.success(doctor_details_data,"New Doctor added successfully")

def get_doctor(database: Session, contact_number : str):
    """Function to tell user if doctor with given contact number already exists or not"""
    return database.query(models.Doctor).filter(models.Doctor.contact_number == contact_number).first()

def get_doctor_by_id(database: Session,patientDatabase: Session,specialist_field,doctor_id):
    """Function to tell user if doctor with given contact number already exists or not"""
    is_doctor_id = False
    if specialist_field == "" and doctor_id != "":
        is_doctor_id = True
        data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == doctor_id,models.Doctor.id == models.DoctorDetails.id).first()
    elif specialist_field == "":
        data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == models.DoctorDetails.id).all()
    else:
        data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == models.DoctorDetails.id,models.DoctorDetails.specialist_field == specialist_field).all()
    list = []
    if is_doctor_id and data is not None:
        dict1 = data["DoctorDetails"]
        dict2 = data["Doctor"]
        dict1.__dict__.update(dict2.__dict__)
        feedback_data = database.query(models.PatientCommentDetails).filter(models.PatientCommentDetails.doctor_id == str(dict1.__dict__["id"])).all()
        if len(feedback_data) > 0:
            for j, ele1 in enumerate(feedback_data):
              db_patient = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(ele1.__dict__["patient_id"])).first()
              if db_patient is not None:
               ele1.__dict__["patient_id"] = db_patient.id
               ele1.__dict__["patient_name"] = db_patient.first_name
              feedback_data[j].__dict__.pop("doctor_id")
              feedback_data[j].__dict__.pop("staff_id")
              feedback_data[j].__dict__.pop("patient_id")
              feedback_data[j].__dict__.pop("hospital_id")
            dict1.__dict__["feedbacks"] = feedback_data
        else:
            dict1.__dict__["feedbacks"] = []
        return ResponseData.success(dict1.__dict__,"Doctor details fetched successfully")
        # list.append(dict1)
    elif (data is not None):
        if(len(data) > 0):
           for i, ele in enumerate(data):
              dict1 = ele["DoctorDetails"]
              dict2 = ele["Doctor"]
              # dict3 = ele["PatientCommentDetails"]
              dict1.__dict__.update(dict2.__dict__)
              # dict1.__dict__["Feedback"] = ele["PatientCommentDetails"]
              list.append(dict1)
    for i, ele in enumerate(list):
        feedback_data = database.query(models.PatientCommentDetails).filter(models.PatientCommentDetails.doctor_id == str(ele.__dict__["id"])).all()
        if len(feedback_data) > 0:
            for j, ele1 in enumerate(feedback_data):
              print(f'ele1.__dict__["patient_id"] {ele1.__dict__["patient_id"]}')
              db_patient = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(ele1.__dict__["patient_id"])).first()
              print(f"db_patient {db_patient}")
              if db_patient is not None:
               ele1.__dict__["patient_id"] = db_patient.id
               ele1.__dict__["patient_name"] = db_patient.first_name
              feedback_data[j].__dict__.pop("doctor_id")
              feedback_data[j].__dict__.pop("staff_id")
              feedback_data[j].__dict__.pop("patient_id")
              feedback_data[j].__dict__.pop("hospital_id")
            ele.__dict__["feedbacks"] = feedback_data
        else:
            ele.__dict__["feedbacks"] = []
    return ResponseData.success(list,"Doctor details fetched successfully")

def get_doctor_by_filter(database: Session,patientDatabase: Session,specialist_field):
    """Function to tell user if doctor with given contact number already exists or not"""
    data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == models.DoctorDetails.id,models.DoctorDetails.specialist_field == specialist_field).all()
    list = []
    if(len(data) > 0):
     for i, ele in enumerate(data):
        dict1 = ele["DoctorDetails"]
        dict2 = ele["Doctor"]
        # dict3 = ele["PatientCommentDetails"]
        dict1.__dict__.update(dict2.__dict__)
        # dict1.__dict__["Feedback"] = ele["PatientCommentDetails"]
        list.append(dict1)
     for i, ele in enumerate(list):
        feedback_data = database.query(models.PatientCommentDetails).filter(models.PatientCommentDetails.doctor_id == str(ele.__dict__["id"])).all()
        if len(feedback_data) > 0:
            for j, ele1 in enumerate(feedback_data):
              print(f'ele1.__dict__["patient_id"] {ele1.__dict__["patient_id"]}')
              db_patient = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(ele1.__dict__["patient_id"])).first()
              print(f"db_patient {db_patient}")
              if db_patient is not None:
               ele1.__dict__["patient_id"] = db_patient.id
               ele1.__dict__["patient_name"] = db_patient.first_name
              feedback_data[j].__dict__.pop("doctor_id")
              feedback_data[j].__dict__.pop("staff_id")
              feedback_data[j].__dict__.pop("patient_id")
              feedback_data[j].__dict__.pop("hospital_id")
            ele.__dict__["feedbacks"] = feedback_data
        else:
            ele.__dict__["feedbacks"] = []
    if len(list) == 0 : 
        return ResponseData.success(list,"No doctor detail found")
    return ResponseData.success(list,"Doctor details fetched successfully")

def delete_doctor_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all doctor details if needed"""
    if id is None:
        database.query(models.Doctor).delete()
        database.commit()
        return ResponseData.success([],"All Doctor details deleted successfully")
    database.query(models.Doctor).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Doctor details deleted successfully")

def add_feeback_of_doctor(database: Session,patientDatabase: Session, comment : Optional[str] = None,rating : Optional[str] = None,patient_id : Optional[str] = None, 
staff_id : Optional[str] = None,doctor_id : Optional[str] = None,
                     hospital_id : Optional[str] = None):
    """Function to add doctor's feedback"""
    # if not check_if_hospital_id_is_valid(database,hospital_id):
    #     raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_patient_id_is_valid(patientDatabase,patient_id):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    if not check_if_doctor_id_is_valid(database,doctor_id):
        raise HTTPException(status_code=400, detail="Doctor id is invalid")
    feedback_data = {
        "comment" : comment,
        "rating" : rating,
        "doctor_id": doctor_id,
  "patient_id": patient_id,
  "staff_id": staff_id,
  "hospital_id": hospital_id,
    }
    db_feedback = models.PatientCommentDetails(**feedback_data)
    database.add(db_feedback)
    database.commit()
    database.refresh(db_feedback)
    return ResponseData.success(db_feedback.__dict__,'New feedback added successfully')

def get_doctor_by_pagination(database: Session,page : int,size:int):
    """Function to get doctor details by pagination"""
    data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == models.DoctorDetails.id).all()
    listdata = []
    if(len(data) > 1):
         for i, ele in enumerate(data):
            dict1 = ele["DoctorDetails"]
            dict2 = ele["Doctor"]
            dict1.__dict__.update(dict2.__dict__)
            listdata.append(dict1)      
         data = listdata[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Doctor details fetched successfully")
         return ResponseData.success([],"No Doctor found")      
    return ResponseData.success(listdata,"No Doctor found")

def update_fields(actualDict,key,value):
    if key != '' or key is not None:
        actualDict[f"{key}"] = value

def update_doctor_details(database: Session,patientDatabase: Session,file: UploadFile, first_name: str, last_name: str, contact_number: str,
                      email: str,gender: str,
                      date_of_birth: str, blood_group: str,
                      years_of_experience: str,next_available_at: str, specialist_field: str, education: str,about : str,hospital_id:str,
                      in_clinic_appointment_fees: str,rating:str, doctor_id: Integer):
    """Function to update doctor details"""
    db_doctor = database.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        return ResponseData.success({},"Doctor with this id does not exists")
    dict2 = {
        "first_name": first_name if first_name != "" else db_doctor.first_name,
  "last_name": last_name if last_name != "" else db_doctor.last_name,
  "contact_number": contact_number if contact_number != "" else db_doctor.contact_number,
  'profile_pic' : f"doctor/app/doctor_images/{file}" if file != "" else f"{db_doctor.profile_pic}",
  "email": email if email != "" else db_doctor.email,
#   "password": password if password != "" else db_doctor.password,
  "gender": gender if gender != "" else db_doctor.gender,
  "date_of_birth": date_of_birth if date_of_birth != "" else db_doctor.date_of_birth,
  "blood_group": blood_group if blood_group != "" else db_doctor.blood_group,
  "hospital_id": hospital_id if hospital_id != "" else db_doctor.hospital_id,
    }
    for key,value in dict2.items():
        update_fields(dict2,key,value)
    db_doctor_details = database.query(models.DoctorDetails).filter(models.DoctorDetails.id == doctor_id).first()
    dict1 = {
        "years_of_experience":years_of_experience if years_of_experience != "" else db_doctor_details.years_of_experience,
  "next_available_at": next_available_at if next_available_at != "" else db_doctor_details.next_available_at,
  "specialist_field": specialist_field if specialist_field != "" else db_doctor_details.specialist_field,
  "education": education if education != "" else db_doctor_details.education,
  "about": about if about != "" else db_doctor_details.about,
  "in_clinic_appointment_fees": in_clinic_appointment_fees if in_clinic_appointment_fees != "" else db_doctor_details.in_clinic_appointment_fees,
  "create_at" : "",
#   "rating" : rating if rating != "" else db_doctor_details.rating,
    }
    database.query(models.Doctor).filter(models.Doctor.id == doctor_id).update({ models.Doctor.id : doctor_id,
        models.Doctor.first_name: dict2["first_name"],
        models.Doctor.last_name : dict2["last_name"],
        models.Doctor.contact_number : dict2["contact_number"],
        models.Doctor.profile_pic : dict2["profile_pic"],
        models.Doctor.email : dict2["email"],
        # models.Doctor.password : dict2["password"],
        models.Doctor.hospital_id : dict2["hospital_id"],
        models.Doctor.gender : dict2["gender"],
        models.Doctor.date_of_birth : dict2["date_of_birth"],
        models.Doctor.blood_group : dict2["blood_group"]
    })
    database.query(models.DoctorDetails).filter(models.DoctorDetails.id == doctor_id).update({
        models.DoctorDetails.id : doctor_id,
        models.DoctorDetails.years_of_experience : dict1["years_of_experience"],
        models.DoctorDetails.next_available_at : dict1["next_available_at"],
        models.DoctorDetails.specialist_field : dict1["specialist_field"],
        models.DoctorDetails.education : dict1["education"],
        models.DoctorDetails.about : dict1["about"],
        models.DoctorDetails.in_clinic_appointment_fees : dict1["in_clinic_appointment_fees"],
        models.DoctorDetails.create_at : dict1["create_at"],
        # models.DoctorDetails.rating : dict1["rating"],
    })
    database.flush()
    database.commit()
    data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == doctor_id,models.Doctor.id == models.DoctorDetails.id).first()
    dict1 = data["DoctorDetails"]
    dict2 = data["Doctor"]
    # dict3 = ele["PatientCommentDetails"]
    dict1.__dict__.update(dict2.__dict__)
    # dict1.__dict__["Feedback"] = ele["PatientCommentDetails"]
    feedback_data = database.query(models.PatientCommentDetails).filter(models.PatientCommentDetails.doctor_id == str(dict1.__dict__["id"])).all()
    if len(feedback_data) > 0:
        for j, ele1 in enumerate(feedback_data):
          print(f'ele1.__dict__["patient_id"] {ele1.__dict__["patient_id"]}')
          db_patient = patientDatabase.query(patientModels.Patient).filter(patientModels.Patient.id == int(ele1.__dict__["patient_id"])).first()
          print(f"db_patient {db_patient}")
          if db_patient is not None:
           ele1.__dict__["patient_id"] = db_patient.id
           ele1.__dict__["patient_name"] = db_patient.first_name
          feedback_data[j].__dict__.pop("doctor_id")
          feedback_data[j].__dict__.pop("staff_id")
          feedback_data[j].__dict__.pop("patient_id")
          feedback_data[j].__dict__.pop("hospital_id")
        dict1.__dict__["feedbacks"] = feedback_data
    else:
        dict1.__dict__["feedbacks"] = []
    return ResponseData.success(dict1.__dict__,"Doctor details updated successfully")

async def doctor_forget_password(database: Session, email : Optional[str] = None):
    """Function to tell user if doctor with given contact number already exists or not"""
    db_doctor_email = database.query(models.Doctor).filter(models.Doctor.email == email).first()
    if not db_doctor_email:
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
    db_patient_otp = database.query(models.Doctor_Otp_For_Password).filter(models.Doctor_Otp_For_Password.doctor_id == db_doctor_email.id).first()
    if db_patient_otp:
        database.query(models.Doctor_Otp_For_Password).filter(db_patient_otp.doctor_id == db_doctor_email.id).update({ 
        models.Doctor_Otp_For_Password.doctor_id : db_doctor_email.id,
        models.Doctor_Otp_For_Password.otp: OTP,
        models.Doctor_Otp_For_Password.updated_at: str(datetime.now()),
    })
        database.flush()
        database.commit()
    else:
        doctor_data = {
        "doctor_id" : db_doctor_email.id,
        "otp" : OTP,
        "created_at" : str(datetime.now())
    }
        db_doctor = models.Doctor_Otp_For_Password(**doctor_data)
        database.add(db_doctor)
        database.commit()
        database.refresh(db_doctor)
    return ResponseData.success_without_data("Otp has been successfully sent on doctor's email address")


def reset_password_for_doctor(database: Session, otp : str,new_password : str):
    """Function to reset password for a particular doctor"""
    doctor_otp_data = database.query(models.Doctor_Otp_For_Password).filter(models.Doctor_Otp_For_Password.otp == otp).first()
    if not doctor_otp_data:
        return ResponseData.failure_without_data("Otp entered is invalid")
    fmt = '%Y-%m-%d %H:%M:%S'
    current_date = datetime.strptime(str(datetime.now()).split(".")[0],fmt)
    if doctor_otp_data.updated_at is not None:
        otp_generated_date = datetime.strptime(str(doctor_otp_data.updated_at).split(".")[0],fmt)
    else:
        otp_generated_date = datetime.strptime(str(doctor_otp_data.created_at).split(".")[0],fmt)
    diff = current_date - otp_generated_date
    if diff.seconds > 60 : 
        database.query(models.Doctor_Otp_For_Password).filter(models.Doctor_Otp_For_Password.doctor_id == doctor_otp_data.doctor_id).delete()
        database.commit()
        return ResponseData.success_without_data("Entered otp is expired or is invalid")
    database.query(models.Doctor).filter(models.Doctor.id == doctor_otp_data.doctor_id).update({
        models.Doctor.password : new_password,     
    })
    database.flush()
    database.commit()
    return ResponseData.success_without_data("Password has been updated successfully")

def doctor_sign_in_api(database: Session,email : Optional[str] = None,password : Optional[str] = None):
    """Function to sign in a doctor"""
    db_doctor = database.query(models.Doctor).filter(models.Doctor.email == email,models.Doctor.password == password).first()
    if not db_doctor:
        return ResponseData.error("Credentials are invalid")
    db_doctor_details = database.query(models.Doctor).filter(models.Doctor.email == email).first()
    token = {
        'authentication_token' : JWTUtility.encode_token(db_doctor_details.email,db_doctor_details.contact_number)
    }
    Merge(token, db_doctor_details.__dict__)
    if db_doctor_details.__dict__["hospital_id"] is None:
        db_doctor_details.__dict__["hospital_id"] = ""
    db_doctor_details.__dict__.pop("password")
    return ResponseData.success(db_doctor_details.__dict__,"Doctor signed in successfully")
