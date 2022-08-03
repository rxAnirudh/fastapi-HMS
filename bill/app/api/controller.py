import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.api.controller import check_if_patient_id_is_valid



# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_bill(database: Session, bill: schemas.BillBase):
    """Function to return query based data while creating new bill creation api"""
    if not check_if_hospital_id_is_valid(database,bill.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_patient_id_is_valid(database,bill.dict()["patient_id"]):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    db_bill = models.Bill(**bill.__dict__)
    database.add(db_bill)
    database.commit()
    database.refresh(db_bill)
    return ResponseData.success(db_bill.__dict__,"Bill added successfully")

def get_bill_by_id(database: Session, id : Optional[int] = None):
    """Function to get bill details by id"""
    db_bill = database.query(models.Bill).filter(models.Bill.id == id).first()
    if db_bill is None:
        return ResponseData.success([],"Bill with this id does not exists")
    return ResponseData.success(db_bill.__dict__,"Bill details fetched successfully")

def delete_bill_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all bill details if needed"""
    if id is None:
        database.query(models.Bill).delete()
        database.commit()
        return ResponseData.success([],"All Bill details deleted successfully")
    database.query(models.Bill).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Bill details deleted successfully")

def update_bill_details(database: Session, bill: schemas.AddNewBill):
    """Function to update bill details"""
    data = database.query(models.Bill).filter(models.Bill.id == bill.id).all()
    dict1 = data[0]
    print('bill.dict()["nursing_charge"]')
    print(bill.dict()["nursing_charge"])
    if bill.dict()["patient_id"] is not None :
        dict1.__dict__["patient_id"] = bill.dict()["patient_id"]
    if bill.dict()["doctor_charge"] is not None :
        dict1.__dict__["doctor_charge"] = bill.dict()["doctor_charge"]
    if bill.dict()["medicine_charge"] is not None :
        dict1.__dict__["medicine_charge"] = bill.dict()["medicine_charge"]
    if bill.dict()["room_charge"] is not None :
        dict1.__dict__["room_charge"] = bill.dict()["room_charge"]
    if bill.dict()["operation_charge"] is not None :
        dict1.__dict__["operation_charge"] = bill.dict()["operation_charge"]
    if bill.dict()["no_of_days"] is not None :
        dict1.__dict__["no_of_days"] = bill.dict()["no_of_days"]
    if bill.dict()["nursing_charge"] is not None :
        dict1.__dict__["nursing_charge"] = bill.dict()["nursing_charge"]
    if bill.dict()["lab_charge"] is not None :
        dict1.__dict__["lab_charge"] = bill.dict()["lab_charge"]
    if bill.dict()["insurance_number"] is not None :
        dict1.__dict__["insurance_number"] = bill.dict()["insurance_number"]
    if bill.dict()["total_bill"] is not None :
        dict1.__dict__["total_bill"] = bill.dict()["total_bill"]
    if bill.dict()["bill_date"] is not None :
        dict1.__dict__["bill_date"] = bill.dict()["bill_date"]
    database.query(models.Bill).filter(models.Bill.id == bill.id).update({ models.Bill.id : bill.id,
        models.Bill.patient_id: dict1.__dict__["patient_id"],
        models.Bill.doctor_charge : dict1.__dict__["doctor_charge"],
        models.Bill.medicine_charge : dict1.__dict__["medicine_charge"],
        models.Bill.room_charge : dict1.__dict__["room_charge"],
        models.Bill.operation_charge : dict1.__dict__["operation_charge"],
        models.Bill.no_of_days : dict1.__dict__["no_of_days"],
        models.Bill.nursing_charge : dict1.__dict__["nursing_charge"],
        models.Bill.lab_charge : dict1.__dict__["lab_charge"],
        models.Bill.insurance_number : dict1.__dict__["insurance_number"],
        models.Bill.total_bill : dict1.__dict__["total_bill"],
        models.Bill.bill_date : dict1.__dict__["bill_date"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Bill details updated successfully")
