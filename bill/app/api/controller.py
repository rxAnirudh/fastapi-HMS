"""Controller file for writing db queries"""
from typing import List, Optional
import sys,os
from sqlalchemy import Integer
from sqlalchemy.orm import Session
from fastapi import HTTPException
from response import Response as ResponseData
from models import models,schemas
from hospital.app.api.controller import check_if_hospital_id_is_valid
from patient.app.api.controller import check_if_patient_id_is_valid
sys.path.append(os.getcwd())



# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_bill(database: Session, file: list(), patient_id: str, doctor_charge: str, medicine_charge: str,
                      room_charge: str, operation_charge: str,
                      nursing_charge: str, lab_charge: str,
                      insurance_number: str, total_bill: str,
                      bill_date: str, hospital_id: str,
                       no_of_days: str):
    """Function to return query based data while creating new bill creation api"""
    if not check_if_hospital_id_is_valid(database,hospital_id):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_patient_id_is_valid(database,patient_id):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    filedata = ''
    for i in file:
        if len(file) == 1:
           filedata+=i
        elif len(file) > 1:
           filedata+=i+','
    billdata = {
        "patient_id": patient_id,
  "doctor_charge": doctor_charge,
  "medicine_charge": medicine_charge,
  "room_charge": room_charge,
  "operation_charge": operation_charge,
  "no_of_days": no_of_days,
  "nursing_charge": nursing_charge,
  "lab_charge": lab_charge,
  "insurance_number": insurance_number,
  "total_bill": total_bill,
  "bill_photo": filedata,
  "bill_date": bill_date,
  "hospital_id": hospital_id
    }
    db_bill = models.Bill(**billdata)
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

def get_bill_by_pagination(database: Session,page : int,size:int):
    """Function to fetch bill details by pagination"""
    mainData = database.query(models.Bill).filter().all()
    if(len(mainData) > 1):
         data = mainData[page*size : (page*size) + size]
         if len(data) > 0:
                 return ResponseData.success(data,"Bill details fetched successfully")
         return ResponseData.success([],"No Bill found")  
    return ResponseData.success(mainData,"No Bill found")

def delete_bill_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all bill details if needed"""
    if id is None:
        database.query(models.Bill).delete()
        database.commit()
        return ResponseData.success([],"All Bill details deleted successfully")
    database.query(models.Bill).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Bill details deleted successfully")

def update_bill_details(database: Session, file: list(), patient_id: str, doctor_charge: str, medicine_charge: str,
                      room_charge: str, operation_charge: str,
                      nursing_charge: str, lab_charge: str,
                      insurance_number: str, total_bill: str,
                      bill_date: str, hospital_id: str,
                       no_of_days: str,bill_id: Integer):
    """Function to update bill details"""
    data = database.query(models.Bill).filter(models.Bill.id == bill_id).all()
    dict1 = data[0]
    if patient_id != '' :
        dict1.__dict__["patient_id"] = patient_id
    if len(file) > 0 :
        filedata = ''
        for i in file:
            if len(file) == 1:
               filedata+='{0}'.format(i)
            elif len(file) > 1:
               filedata+='{i},'.format(i)
        dict1.__dict__["bill_photo"] = filedata
    if doctor_charge != '' :
        dict1.__dict__["doctor_charge"] = doctor_charge
    if medicine_charge != '' :
        dict1.__dict__["medicine_charge"] = medicine_charge
    if room_charge != '' :
        dict1.__dict__["room_charge"] = room_charge
    if operation_charge != '' :
        dict1.__dict__["operation_charge"] = operation_charge
    if nursing_charge != '' :
        dict1.__dict__["nursing_charge"] = nursing_charge
    if lab_charge != '' :
        dict1.__dict__["lab_charge"] = lab_charge
    if insurance_number != '' :
        dict1.__dict__["insurance_number"] = insurance_number
    if total_bill != '' :
        dict1.__dict__["total_bill"] = total_bill
    if hospital_id != '' :
        dict1.__dict__["hospital_id"] = hospital_id
    if no_of_days != '' :
        dict1.__dict__["no_of_days"] = no_of_days
    database.query(models.Bill).filter(models.Bill.id == bill_id).update({ models.Bill.id : bill_id,
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
        models.Bill.bill_photo : dict1.__dict__["bill_photo"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Bill details updated successfully")
