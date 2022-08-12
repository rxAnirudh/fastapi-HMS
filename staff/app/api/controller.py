import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from staff.app.models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def check_if_staff_id_is_valid(database: Session, id : Optional[int] = None):
    staff_data = database.query(models.Staff).filter(models.Staff.id == id).first()
    if staff_data:
        return True
    else:
        return False

def add_new_staff(database: Session, staff: schemas.StaffBase):
    """Function to return query based data while creating new staff creation api"""
    if not check_if_hospital_id_is_valid(database,staff.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    staff_dict = {'first_name': staff.dict()["first_name"], 'last_name': staff.dict()["last_name"],"contact_number" : staff.dict()["contact_number"],
    "profile_pic" : staff.dict()["profile_pic"],"email" : staff.dict()["email"],"gender" : staff.dict()["gender"],"date_of_birth" : staff.dict()["date_of_birth"],
    "blood_group" : staff.dict()["blood_group"],"hospital_id" : staff.dict()["hospital_id"]}
    db_staff = models.Staff(**staff_dict)
    database.add(db_staff)
    database.commit()
    database.refresh(db_staff)
    staff_details_dict = {'years_of_experience': staff.dict()["years_of_experience"],"education" : staff.dict()["education"],
    "create_at" : staff.dict()["create_at"],"id" : db_staff.id,}
    db_staff_details = models.StaffDetails(**staff_details_dict)
    database.add(db_staff_details)
    database.commit()
    database.refresh(db_staff_details)
    Merge(staff_dict, staff_details_dict)
    return ResponseData.success(staff_details_dict,"Staff created successfully")

def get_staff(database: Session, contact_number : str):
    """Function to tell user if staff with given contact number already exists or not"""
    return database.query(models.Staff).filter(models.Staff.contact_number == contact_number).first()

def get_staff_by_id(database: Session, id : Optional[int] = None):
    """Function to tell user if staff with given contact number already exists or not"""
    db_staff = database.query(models.Staff).filter(models.Staff.id == id).first()
    if db_staff is None:
        return ResponseData.success([],"Staff with this id does not exists")
    db_staff_details = database.query(models.StaffDetails).filter(models.StaffDetails.id == id).first()
    Merge(db_staff.__dict__, db_staff_details.__dict__)
    return ResponseData.success(db_staff_details.__dict__,"Staff details fetched successfully")

def get_staff_by_pagination(database: Session,page : int,size:int):
    """Function to get staff details by pagination"""
    data = database.query(models.Staff,models.StaffDetails).filter(models.Staff.id == models.StaffDetails.id).all()
    listdata = []
    if(len(data) > 1):
         for i, ele in enumerate(data):
            dict1 = ele["StaffDetails"]
            dict2 = ele["Staff"]
            dict1.__dict__.update(dict2.__dict__)
            listdata.append(dict1)      
         data = listdata[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Staff details fetched successfully")
         return ResponseData.success([],"No Staff found")  
    return ResponseData.success(listdata,"No Staff found")

def delete_staff_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all staff details if needed"""
    if id is None:
        database.query(models.Staff).delete()
        database.commit()
        return ResponseData.success([],"All Staff details deleted successfully")
    database.query(models.Staff).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Staff details deleted successfully")

def update_staff_details(database: Session, staff: schemas.AddNewStaff):
    """Function to return query based data while creating add_new_staff creation api"""
    data = database.query(models.StaffDetails,models.Staff).filter(models.Staff.id == staff.id).all()
    dict1 = data[0]["StaffDetails"]
    dict2 = data[0]["Staff"]
    if staff.dict()["first_name"] is not None :
        dict2.__dict__["first_name"] = staff.dict()["first_name"]
    if staff.dict()["last_name"] is not None :
        dict2.__dict__["last_name"] = staff.dict()["last_name"]
    if staff.dict()["contact_number"] is not None :
        dict2.__dict__["contact_number"] = staff.dict()["contact_number"]
    if staff.dict()["profile_pic"] is not None :
        dict2.__dict__["profile_pic"] = staff.dict()["profile_pic"]
    if staff.dict()["email"] is not None :
        dict2.__dict__["email"] = staff.dict()["email"]
    if staff.dict()["gender"] is not None :
        dict2.__dict__["gender"] = staff.dict()["gender"]
    if staff.dict()["date_of_birth"] is not None :
        dict2.__dict__["date_of_birth"] = staff.dict()["date_of_birth"]
    if staff.dict()["blood_group"] is not None :
        dict2.__dict__["blood_group"] = staff.dict()["blood_group"]
    if staff.dict()["hospital_id"] is not None :
        dict2.__dict__["hospital_id"] = staff.dict()["hospital_id"]
    if staff.dict()["years_of_experience"] is not None :
        dict1.__dict__["years_of_experience"] = staff.dict()["years_of_experience"]
    if staff.dict()["education"] is not None :
        dict1.__dict__["education"] = staff.dict()["education"]
    if staff.dict()["create_at"] is not None :
        dict1.__dict__["create_at"] = staff.dict()["create_at"]
    database.query(models.Staff).filter(models.Staff.id == staff.id).update({ models.Staff.id : staff.id,
        models.Staff.first_name: dict2.__dict__["first_name"],
        models.Staff.last_name : dict2.__dict__["last_name"],
        models.Staff.contact_number : dict2.__dict__["contact_number"],
        models.Staff.profile_pic : dict2.__dict__["profile_pic"],
        models.Staff.email : dict2.__dict__["email"],
        models.Staff.gender : dict2.__dict__["gender"],
        models.Staff.date_of_birth : dict2.__dict__["date_of_birth"],
        models.Staff.blood_group : dict2.__dict__["blood_group"],
        models.Staff.hospital_id : dict2.__dict__["hospital_id"],
    })
    database.query(models.StaffDetails).filter(models.StaffDetails.id == staff.id).update({
        models.StaffDetails.id : staff.id,
        models.StaffDetails.years_of_experience : dict1.__dict__["years_of_experience"],
        models.StaffDetails.education : dict1.__dict__["education"],
        models.StaffDetails.create_at : dict1.__dict__["create_at"]
    })
    database.flush()
    database.commit()
    dict1.__dict__.update(dict2.__dict__)
    return ResponseData.success(dict1.__dict__,"Staff details updated successfully")
