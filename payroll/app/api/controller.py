import sys
import os
from fastapi import HTTPException
from sqlalchemy import Integer
sys.path.append(os.getcwd())
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

def add_new_payroll(database: Session, file: list(), staff_id: str, salary: str, net_salary: str,
                      hourly_salary: str, bonus_salary: str,
                      compensation: str, account_no: str,
                      hospital_id: str):
    """Function to add new payroll of staff working in hospital"""
    if not check_if_hospital_id_is_valid(database,hospital_id):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_staff_id_is_valid(database,staff_id):
        raise HTTPException(status_code=400, detail="Staff id is invalid")
    filedata = ''
    for i in file:
        if len(file) == 1:
           filedata+=i
        elif len(file) > 1:
           filedata+=i+','
    payrolldata = {
        "staff_id": staff_id,
  "net_salary": net_salary,
  "hourly_salary": hourly_salary,
  "bonus_salary": bonus_salary,
  "compensation": compensation,
  "account_no": account_no,
  "hospital_id": hospital_id,
  'payroll_slip' : filedata
    }
    db_payroll = models.Payroll(**payrolldata)
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

def update_payroll_details(database: Session, file: list(), staff_id: str, salary: str, net_salary: str,
                      hourly_salary: str, bonus_salary: str,
                      compensation: str, account_no: str,
                      hospital_id: str,payroll_id: Integer):
    """Function to update payroll details"""
    data = database.query(models.Payroll).filter(models.Payroll.id == payroll_id).all()
    dict1 = data[0]
    if staff_id != '' :
        dict1.__dict__["staff_id"] = staff_id
    if len(file) > 0 :
        filedata = ''
        for i in file:
            if len(file) == 1:
               filedata+='{0}'.format(i)
            elif len(file) > 1:
               filedata+='{i},'.format(i)
        dict1.__dict__["payroll_slip"] = filedata
    if salary != '' :
        dict1.__dict__["salary"] = salary
    if net_salary != '' :
        dict1.__dict__["net_salary"] = net_salary
    if hourly_salary != '' :
        dict1.__dict__["hourly_salary"] = hourly_salary
    if bonus_salary != '' :
        dict1.__dict__["bonus_salary"] = bonus_salary
    if compensation != '' :
        dict1.__dict__["compensation"] = compensation
    if account_no != '' :
        dict1.__dict__["account_no"] = account_no
    if hospital_id != '' :
        dict1.__dict__["hospital_id"] = hospital_id
    database.query(models.Payroll).filter(models.Payroll.id == payroll_id).update({ models.Payroll.id : payroll_id,
        models.Payroll.staff_id: dict1.__dict__["staff_id"],
        models.Payroll.salary : dict1.__dict__["salary"],
        models.Payroll.net_salary : dict1.__dict__["net_salary"],
        models.Payroll.hourly_salary : dict1.__dict__["hourly_salary"],
        models.Payroll.bonus_salary : dict1.__dict__["bonus_salary"],
        models.Payroll.compensation : dict1.__dict__["compensation"],
        models.Payroll.account_no : dict1.__dict__["account_no"],
        models.Payroll.hospital_id : dict1.__dict__["hospital_id"],
        models.Payroll.payroll_slip : dict1.__dict__["payroll_slip"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Payroll details updated successfully")
