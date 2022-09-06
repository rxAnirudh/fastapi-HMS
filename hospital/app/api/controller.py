"""Controller file for writing db queries"""
import sys,os
sys.path.append(os.getcwd())
from typing import Optional
from sqlalchemy.orm import Session
from hospital.app.models.schemas import HospitalBase, HospitalCreate
from hospital.app.models.models import Hospital,HospitalDetails
from hospital.app.response import Response as ResponseData
from hospital.app.error_handling import Error

# Python code to merge dict using update() method
def Merge(dict1, dict2):
    return(dict2.update(dict1))


def create_hospital(database: Session, hospital: HospitalBase):
    """Function to return query based data while creating new_hospital creation api"""
    for key,value in hospital.dict().items():
        is_error = Error.if_param_is_null_or_empty(hospital.dict()[key],key)
        if is_error:
            return ResponseData.success_without_data(f"{key} cannot be empty")
    hospital_name = database.query(Hospital).filter(str(Hospital.name).lower() == str(hospital.dict()["name"]).lower()).first()
    if hospital_name:
        return ResponseData.success_without_data("Hopital with same name already exists")
    hospital_dict = {'name': hospital.dict()["name"], 'address': hospital.dict()["address"],"city" : hospital.dict()["city"],
    "pincode" : hospital.dict()["pincode"],"state" : hospital.dict()["state"],"country" : hospital.dict()["country"]}
    db_hospital = Hospital(**hospital_dict)
    database.add(db_hospital)
    database.commit()
    database.refresh(db_hospital)
    hospital_details_dict = {'hospital_type': hospital.dict()["hospital_type"], 'is_rented': hospital.dict()["is_rented"],"contact_number" : hospital.dict()["contact_number"],
    "email" : hospital.dict()["email"],"id" : db_hospital.id}
    db_hospital_details = HospitalDetails(**hospital_details_dict)
    database.add(db_hospital_details)
    database.commit()
    database.refresh(db_hospital_details)
    Merge(hospital_dict, hospital_details_dict)
    return ResponseData.success(hospital_details_dict,"Hospital created successfully")

def get_hospital(database: Session, contact_number : str):
    """Function to tell user if hospital with given contact number already exists or not"""
    return database.query(HospitalDetails).filter(HospitalDetails.contact_number == contact_number).first()

def check_if_hospital_id_is_valid(database: Session, id : Optional[int] = None):
    hospital_data = database.query(Hospital).filter(Hospital.id == id).first()
    if hospital_data:
        return True
    else:
        return False

def get_hospital_by_id(database: Session, id : Optional[int] = None):
    """Function to tell user if hospital with given contact number already exists or not"""
    if id is None:
        data = database.query(HospitalDetails,Hospital).filter(Hospital.id == HospitalDetails.id).all()
        list = []
        if(len(data) > 1):
         for i, ele in enumerate(data):
            dict1 = ele["HospitalDetails"]
            dict2 = ele["Hospital"]
            dict1.__dict__.update(dict2.__dict__)
            list.append(dict1)
        return ResponseData.success(list,"Hospital details fetched successfully")
    db_hospital = database.query(Hospital).filter(Hospital.id == id).first()
    if db_hospital is None:
        return ResponseData.success([],"Hospital with this id does not exists")
    db_hospital_details = database.query(HospitalDetails).filter(HospitalDetails.id == id).first()
    Merge(db_hospital.__dict__, db_hospital_details.__dict__)
    return ResponseData.success(db_hospital_details.__dict__,"Hospital details fetched successfully")

def search_hospital_by_name(database: Session, hospital_name : Optional[str] = None):
    """Function to get list of all hospital based on name search"""
    data = database.query(HospitalDetails,Hospital).filter(Hospital.id == HospitalDetails.id).all()
    list = []
    if(len(data) > 1):
     for i, ele in enumerate(data):
        dict1 = ele["HospitalDetails"]
        dict2 = ele["Hospital"]
        if hospital_name in dict2.__dict__["name"]:
           dict1.__dict__.update(dict2.__dict__)
           list.append(dict1)
    if len(list) == 0:
        return ResponseData.success(list,"No hospital found with this name")
    return ResponseData.success(list,"Hospital details fetched successfully")

def delete_hospital(database: Session, id : Optional[int] = None):
    """Function to delete single or all hospitals if needed"""
    if id is None:
        database.query(Hospital).delete()
        database.commit()
        return ResponseData.success([],"All hospitals deleted successfully")
    database.query(Hospital).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Hospital deleted successfully")

def get_hospital_by_pagination(database: Session,page : int,size:int):
    """Function to delete single or all hospitals if needed"""
    data = database.query(HospitalDetails,Hospital).filter(Hospital.id == HospitalDetails.id).all()
    listdata = []
    if(len(data) > 1):
         for i, ele in enumerate(data):
            dict1 = ele["HospitalDetails"]
            dict2 = ele["Hospital"]
            dict1.__dict__.update(dict2.__dict__)
            listdata.append(dict1)      
         data = listdata[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Hospital details fetched successfully")
         return ResponseData.success([],"No hospital found")  
    return ResponseData.success(listdata,"No hospital found")

def update_hospital(database: Session, hospital: HospitalCreate):
    """Function to return query based data while creating new_hospital creation api"""
    data = database.query(HospitalDetails,Hospital).filter(Hospital.id == hospital.id).all()
    dict1 = data[0]["HospitalDetails"]
    dict2 = data[0]["Hospital"]
    if hospital.dict()["name"] is not None :
        dict2.__dict__["name"] = hospital.dict()["name"]
    if hospital.dict()["address"] is not None :
        dict2.__dict__["address"] = hospital.dict()["address"]
    if hospital.dict()["city"] is not None :
        dict2.__dict__["city"] = hospital.dict()["city"]
    if hospital.dict()["pincode"] is not None :
        dict2.__dict__["pincode"] = hospital.dict()["pincode"]
    if hospital.dict()["state"] is not None :
        dict2.__dict__["state"] = hospital.dict()["state"]
    if hospital.dict()["country"] is not None :
        dict2.__dict__["country"] = hospital.dict()["country"]
    if hospital.dict()["hospital_type"] is not None :
        dict1.__dict__["hospital_type"] = hospital.dict()["hospital_type"]
    if hospital.dict()["is_rented"] is not None :
        dict1.__dict__["is_rented"] = hospital.dict()["is_rented"]
    if hospital.dict()["contact_number"] is not None :
        dict1.__dict__["contact_number"] = hospital.dict()["contact_number"]
    if hospital.dict()["email"] is not None :
        dict1.__dict__["email"] = hospital.dict()["email"]
    database.query(Hospital).filter(Hospital.id == hospital.id).update({ Hospital.id : hospital.id,
        Hospital.name: dict2.__dict__["name"],
        Hospital.address : dict2.__dict__["address"],
        Hospital.pincode : dict2.__dict__["pincode"],
        Hospital.city : dict2.__dict__["city"],
        Hospital.state : dict2.__dict__["state"],
        Hospital.country : dict2.__dict__["country"]
    })
    database.query(HospitalDetails).filter(HospitalDetails.id == hospital.id).update({
        HospitalDetails.id : hospital.id,
        HospitalDetails.hospital_type : dict1.__dict__["hospital_type"],
        HospitalDetails.is_rented : dict1.__dict__["is_rented"],
        HospitalDetails.contact_number : dict1.__dict__["contact_number"],
        HospitalDetails.email : dict1.__dict__["email"],
        HospitalDetails.create_at : dict1.__dict__["create_at"]
    })
    database.flush()
    database.commit()
    dict1.__dict__.update(dict2.__dict__)
    return ResponseData.success(dict1.__dict__,"Hospital details updated successfully")