"""Controller file for writing db queries"""
from typing import Optional
from sqlalchemy.orm import Session
from doctor.app.error_handling import Error
from response import Response as ResponseData
from doctor.app.models import models,schemas


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

def add_new_doctor(database: Session, doctor: schemas.DoctorBase):
    """Function to return query based data while creating new doctor creation api"""
    for key,value in doctor.dict().items():
        is_error = Error.if_param_is_null_or_empty(doctor.dict()[key],key)
        if is_error:
            return ResponseData.success_without_data(f"{key} cannot be empty")
    doctor_dict = {'first_name': doctor.dict()["first_name"], 'last_name': doctor.dict()["last_name"],"contact_number" : doctor.dict()["contact_number"],
    "profile_pic" : doctor.dict()["profile_pic"],"email" : doctor.dict()["email"],"gender" : doctor.dict()["gender"],"date_of_birth" : doctor.dict()["date_of_birth"],
    "blood_group" : doctor.dict()["blood_group"]}
    db_doctor = models.Doctor(**doctor_dict)
    database.add(db_doctor)
    database.commit()
    database.refresh(db_doctor)
    doctor_details_dict = {'years_of_experience': doctor.dict()["years_of_experience"], 'next_available_at': doctor.dict()["next_available_at"],"specialist_field" : doctor.dict()["specialist_field"],
    "education" : doctor.dict()["education"],"id" : db_doctor.id,"in_clinic_appointment_fees" : doctor.dict()["in_clinic_appointment_fees"],"create_at" : doctor.dict()["create_at"]}
    db_doctor_details = models.DoctorDetails(**doctor_details_dict)
    database.add(db_doctor_details)
    database.commit()
    database.refresh(db_doctor_details)
    Merge(doctor_dict, doctor_details_dict)
    # patient_comments_dict = {'patients_comment': doctor.dict()["patients_comment"],"id" : db_doctor.id}
    # db_patient_details = models.PatientCommentDetails(**patient_comments_dict)
    # database.add(db_patient_details)
    # database.commit()
    # database.refresh(db_patient_details)
    return ResponseData.success(doctor_details_dict,"Doctor created successfully")

def get_doctor(database: Session, contact_number : str):
    """Function to tell user if doctor with given contact number already exists or not"""
    return database.query(models.Doctor).filter(models.Doctor.contact_number == contact_number).first()

def get_doctor_by_id(database: Session, id : Optional[int] = None):
    """Function to tell user if doctor with given contact number already exists or not"""
    # if id is None:
    #     data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == models.DoctorDetails.id).all()
    #     list = []
    #     if(len(data) > 1):
    #      for i, ele in enumerate(data):
    #         dict1 = ele["DoctorDetails"]
    #         dict2 = ele["Doctor"]
    #         dict1.__dict__.update(dict2.__dict__)
    #         list.append(dict1)
    #     return ResponseData.success(list,"Doctor details fetched successfully")
    db_doctor = database.query(models.Doctor).filter(models.Doctor.id == id).first()
    if db_doctor is None:
        return ResponseData.success([],"Doctor with this id does not exists")
    db_doctor_details = database.query(models.DoctorDetails).filter(models.DoctorDetails.id == id).first()
    Merge(db_doctor.__dict__, db_doctor_details.__dict__)
    return ResponseData.success(db_doctor_details.__dict__,"Doctor details fetched successfully")

def delete_doctor_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all doctor details if needed"""
    if id is None:
        database.query(models.Doctor).delete()
        database.commit()
        return ResponseData.success([],"All Doctor details deleted successfully")
    database.query(models.Doctor).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Doctor details deleted successfully")

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

def update_doctor_details(database: Session, doctor: schemas.AddNewDoctor):
    """Function to return query based data while creating add_new_doctor creation api"""
    data = database.query(models.DoctorDetails,models.Doctor).filter(models.Doctor.id == doctor.id).all()
    dict1 = data[0]["DoctorDetails"]
    dict2 = data[0]["Doctor"]
    # dict3 = data[0]["PatientCommentDetails"]
    if doctor.dict()["first_name"] is not None :
        dict2.__dict__["first_name"] = doctor.dict()["first_name"]
    if doctor.dict()["last_name"] is not None :
        dict2.__dict__["last_name"] = doctor.dict()["last_name"]
    if doctor.dict()["contact_number"] is not None :
        dict2.__dict__["contact_number"] = doctor.dict()["contact_number"]
    if doctor.dict()["profile_pic"] is not None :
        dict2.__dict__["profile_pic"] = doctor.dict()["profile_pic"]
    if doctor.dict()["email"] is not None :
        dict2.__dict__["email"] = doctor.dict()["email"]
    if doctor.dict()["gender"] is not None :
        dict2.__dict__["gender"] = doctor.dict()["gender"]
    if doctor.dict()["date_of_birth"] is not None :
        dict2.__dict__["date_of_birth"] = doctor.dict()["date_of_birth"]
    if doctor.dict()["blood_group"] is not None :
        dict2.__dict__["blood_group"] = doctor.dict()["blood_group"]
    if doctor.dict()["years_of_experience"] is not None :
        dict1.__dict__["years_of_experience"] = doctor.dict()["years_of_experience"]
    if doctor.dict()["next_available_at"] is not None :
        dict1.__dict__["next_available_at"] = doctor.dict()["next_available_at"]
    if doctor.dict()["specialist_field"] is not None :
        dict1.__dict__["specialist_field"] = doctor.dict()["specialist_field"]
    if doctor.dict()["education"] is not None :
        dict1.__dict__["education"] = doctor.dict()["education"]
    if doctor.dict()["in_clinic_appointment_fees"] is not None :
        dict1.__dict__["in_clinic_appointment_fees"] = doctor.dict()["in_clinic_appointment_fees"]
    if doctor.dict()["create_at"] is not None :
        dict1.__dict__["create_at"] = doctor.dict()["create_at"]
    # if doctor.dict()["patients_comment"] is not None :
    #     dict3.__dict__["patients_comment"] = doctor.dict()["patients_comment"]
    database.query(models.Doctor).filter(models.Doctor.id == doctor.id).update({ models.Doctor.id : doctor.id,
        models.Doctor.first_name: dict2.__dict__["first_name"],
        models.Doctor.last_name : dict2.__dict__["last_name"],
        models.Doctor.contact_number : dict2.__dict__["contact_number"],
        models.Doctor.profile_pic : dict2.__dict__["profile_pic"],
        models.Doctor.email : dict2.__dict__["email"],
        models.Doctor.gender : dict2.__dict__["gender"],
        models.Doctor.date_of_birth : dict2.__dict__["date_of_birth"],
        models.Doctor.blood_group : dict2.__dict__["blood_group"]
    })
    database.query(models.DoctorDetails).filter(models.DoctorDetails.id == doctor.id).update({
        models.DoctorDetails.id : doctor.id,
        models.DoctorDetails.years_of_experience : dict1.__dict__["years_of_experience"],
        models.DoctorDetails.next_available_at : dict1.__dict__["next_available_at"],
        models.DoctorDetails.specialist_field : dict1.__dict__["specialist_field"],
        models.DoctorDetails.education : dict1.__dict__["education"],
        models.DoctorDetails.in_clinic_appointment_fees : dict1.__dict__["in_clinic_appointment_fees"],
        models.DoctorDetails.create_at : dict1.__dict__["create_at"]
    })
    # database.query(models.PatientCommentDetails).filter(models.PatientCommentDetails.doctor_id == doctor.id).update({ models.PatientCommentDetails.doctor_id : doctor.id,
    #     models.PatientCommentDetails.patients_comment: dict3.__dict__["patients_comment"],
    #     models.PatientCommentDetails.user_id : dict3.__dict__["user_id"]
    # })
    database.flush()
    database.commit()
    dict1.__dict__.update(dict2.__dict__)
    # dict1.__dict__.update(dict3.__dict__)
    return ResponseData.success(dict1.__dict__,"Doctor details updated successfully")
