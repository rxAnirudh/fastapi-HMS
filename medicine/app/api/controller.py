import sys

from fastapi import HTTPException

from medicine.app.error_handling import Error
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from medicine.app.models import models,schemas
from response import Response as ResponseData


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_medicine(database: Session, medicine: schemas.MedicineBase):
    """Function to return query based data while creating new medicine creation api"""
    for key,value in medicine.dict().items():
        if key == "name" or key == "cost" or key == "production_date":
            is_error = Error.if_param_is_null_or_empty(medicine.dict()[key],key)
            if is_error:
                return ResponseData.success_without_data(f"{key} cannot be empty")
    medicine_dict = {'name': medicine.dict()["name"], 'type': medicine.dict()["type"],"cost" : medicine.dict()["cost"],
    "description" : medicine.dict()["description"]}
    db_medicine = models.Medicine(**medicine_dict)
    database.add(db_medicine)
    database.commit()
    database.refresh(db_medicine)
    medicine_report_dict = {'company': medicine.dict()["company"],"quantity" : medicine.dict()["quantity"],
    "production_date" : medicine.dict()["production_date"],"expire_date" : medicine.dict()["expire_date"],
    "country" : medicine.dict()["country"],
    "supplier_id" : medicine.dict()["supplier_id"],"id" : db_medicine.id,}
    db_medicine_report = models.MedicineReport(**medicine_report_dict)
    database.add(db_medicine_report)
    database.commit()
    database.refresh(db_medicine_report)
    Merge(medicine_dict, medicine_report_dict)
    return ResponseData.success(medicine_report_dict,"Medicine added successfully")

def get_medicine_by_id(database: Session, id : Optional[int] = None):
    """Function to tell user if medicine with given id already exists or not"""
    db_medicine = database.query(models.Medicine).filter(models.Medicine.id == id).first()
    if db_medicine is None:
        return ResponseData.success([],"Medicine with this id does not exists")
    db_medicine_report = database.query(models.MedicineReport).filter(models.MedicineReport.id == id).first()
    Merge(db_medicine.__dict__, db_medicine_report.__dict__)
    return ResponseData.success(db_medicine_report.__dict__,"Medicine details fetched successfully")

def get_medicine_by_pagination(database: Session,page : int,size:int):
    """Function to get medicine details by pagination"""
    data = database.query(models.Medicine,models.MedicineReport).filter(models.Medicine.id == models.MedicineReport.id).all()
    listdata = []
    if(len(data) > 1):
         for i, ele in enumerate(data):
            dict1 = ele["MedicineReport"]
            dict2 = ele["Medicine"]
            dict1.__dict__.update(dict2.__dict__)
            listdata.append(dict1)      
         data = listdata[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Medicine details fetched successfully")
         return ResponseData.success([],"No Medicine found")  
    return ResponseData.success(listdata,"No Medicine found")

def delete_medicine_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all medicine details if needed"""
    if id is None:
        database.query(models.Medicine).delete()
        database.commit()
        return ResponseData.success([],"All Medicine details deleted successfully")
    database.query(models.Medicine).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Medicine details deleted successfully")

def update_medicine_details(database: Session, medicine: schemas.AddNewMedicine):
    """Function to return query based data while creating add_new_medicine creation api"""
    data = database.query(models.MedicineReport,models.Medicine).filter(models.Medicine.id == medicine.id).all()
    dict1 = data[0]["MedicineReport"]
    dict2 = data[0]["Medicine"]
    if medicine.dict()["name"] is not None :
        dict2.__dict__["name"] = medicine.dict()["name"]
    if medicine.dict()["type"] is not None :
        dict2.__dict__["type"] = medicine.dict()["type"]
    if medicine.dict()["cost"] is not None :
        dict2.__dict__["cost"] = medicine.dict()["cost"]
    if medicine.dict()["description"] is not None :
        dict2.__dict__["description"] = medicine.dict()["description"]
    if medicine.dict()["company"] is not None :
        dict1.__dict__["company"] = medicine.dict()["company"]
    if medicine.dict()["quantity"] is not None :
        dict1.__dict__["quantity"] = medicine.dict()["quantity"]
    if medicine.dict()["production_date"] is not None :
        dict1.__dict__["production_date"] = medicine.dict()["production_date"]
    if medicine.dict()["expire_date"] is not None :
        dict1.__dict__["expire_date"] = medicine.dict()["expire_date"]
    if medicine.dict()["country"] is not None :
        dict1.__dict__["country"] = medicine.dict()["country"]
    if medicine.dict()["supplier_id"] is not None :
        dict1.__dict__["supplier_id"] = medicine.dict()["supplier_id"]
    database.query(models.Medicine).filter(models.Medicine.id == medicine.id).update({ models.Medicine.id : medicine.id,
        models.Medicine.name: dict2.__dict__["name"],
        models.Medicine.type : dict2.__dict__["type"],
        models.Medicine.cost : dict2.__dict__["cost"],
        models.Medicine.description : dict2.__dict__["description"],
    })
    database.query(models.MedicineReport).filter(models.MedicineReport.id == medicine.id).update({
        models.MedicineReport.id : medicine.id,
        models.MedicineReport.company : dict1.__dict__["company"],
        models.MedicineReport.quantity : dict1.__dict__["quantity"],
        models.MedicineReport.production_date : dict1.__dict__["production_date"],
        models.MedicineReport.expire_date : dict1.__dict__["expire_date"],
        models.MedicineReport.country : dict1.__dict__["country"],
        models.MedicineReport.supplier_id : dict1.__dict__["supplier_id"]    
    })
    database.flush()
    database.commit()
    dict1.__dict__.update(dict2.__dict__)
    return ResponseData.success(dict1.__dict__,"Medicine details updated successfully")
