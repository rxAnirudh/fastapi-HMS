"""File for patient route"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from payroll.app.models import schemas
from db import get_db

from api import controller

payroll_router = APIRouter()


@payroll_router.post("/add_payroll", response_model=schemas.AddPayrollResponse)
def add_payroll(payroll: schemas.PayrollBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new payroll details"""
    return controller.add_new_payroll(database,payroll)


@payroll_router.post("/get_payroll_details")
def get_payroll_details(payrollid: schemas.PayrollId, database: Session = Depends(get_db)):
    """Function to return payroll details
    (specific and all payroll data can be fetched)"""
    return controller.get_payroll_by_id(database, id = payrollid.id)


@payroll_router.post("/delete_payroll_details")
def delete_payroll_details(payrollid: schemas.PayrollId, database: Session = Depends(get_db)):
    """Function to return payroll details
    (specific and all payroll data can be fetched)"""
    return controller.delete_payroll_details(database, id = payrollid.id)


@payroll_router.post("/update_payroll_details")
def update_payroll_details(payroll_details: schemas.AddNewPayroll, database: Session = Depends(get_db)):
    """Function to update particular bill details"""
    return controller.update_payroll_details(database, payroll = payroll_details)
