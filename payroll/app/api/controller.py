import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from staff.app.api.controller import check_if_staff_id_is_valid



# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_payroll(database: Session, payroll: schemas.PayrollBase):
    """Function to add new payroll of staff working in hospital"""
    if not check_if_hospital_id_is_valid(database,payroll.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_staff_id_is_valid(database,payroll.dict()["staff_id"]):
        raise HTTPException(status_code=400, detail="Staff id is invalid")
    db_payroll = models.Payroll(**payroll.__dict__)
    database.add(db_payroll)
    database.commit()
    database.refresh(db_payroll)
    return ResponseData.success(db_payroll.__dict__,"Payroll for this staff added successfully")

def get_payroll_by_id(database: Session, id : Optional[int] = None):
    """Function to get payroll details by id"""
    db_payroll = database.query(models.Payroll).filter(models.Payroll.id == id).first()
    if db_payroll is None:
        return ResponseData.success([],"Payroll with this id does not exists")
    return ResponseData.success(db_payroll.__dict__,"Payroll details fetched successfully")

def delete_payroll_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all payroll details if needed"""
    if id is None:
        database.query(models.Payroll).delete()
        database.commit()
        return ResponseData.success([],"All Payroll details deleted successfully")
    database.query(models.Payroll).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Payroll details deleted successfully")

def update_payroll_details(database: Session, payroll: schemas.AddNewPayroll):
    """Function to update payroll details"""
    data = database.query(models.Payroll).filter(models.Payroll.id == payroll.id).all()
    dict1 = data[0]
    if payroll.dict()["staff_id"] is not None :
        dict1.__dict__["staff_id"] = payroll.dict()["staff_id"]
    if payroll.dict()["salary"] is not None :
        dict1.__dict__["salary"] = payroll.dict()["salary"]
    if payroll.dict()["net_salary"] is not None :
        dict1.__dict__["net_salary"] = payroll.dict()["net_salary"]
    if payroll.dict()["hourly_salary"] is not None :
        dict1.__dict__["hourly_salary"] = payroll.dict()["hourly_salary"]
    if payroll.dict()["bonus_salary"] is not None :
        dict1.__dict__["bonus_salary"] = payroll.dict()["bonus_salary"]
    if payroll.dict()["compensation"] is not None :
        dict1.__dict__["compensation"] = payroll.dict()["compensation"]
    if payroll.dict()["account_no"] is not None :
        dict1.__dict__["account_no"] = payroll.dict()["account_no"]
    if payroll.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = payroll.dict()["hospital_id"]
    database.query(models.Payroll).filter(models.Payroll.id == payroll.id).update({ models.Payroll.id : payroll.id,
        models.Payroll.staff_id: dict1.__dict__["staff_id"],
        models.Payroll.salary : dict1.__dict__["salary"],
        models.Payroll.net_salary : dict1.__dict__["net_salary"],
        models.Payroll.hourly_salary : dict1.__dict__["hourly_salary"],
        models.Payroll.bonus_salary : dict1.__dict__["bonus_salary"],
        models.Payroll.compensation : dict1.__dict__["compensation"],
        models.Payroll.account_no : dict1.__dict__["account_no"],
        models.Payroll.hospital_id : dict1.__dict__["hospital_id"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Payroll details updated successfully")
