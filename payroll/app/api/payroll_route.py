"""File for patient route"""
import os
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends, APIRouter, File, Form, UploadFile
from sqlalchemy.orm import Session
from payroll.app.models import schemas
from db import get_db

from api import controller

payroll_router = APIRouter()

IMAGE_DIR_PATH = "/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/payroll/payroll_slips"

async def create_file(file=File(None)):
    try:
        contents = await file.read()
        path = os.path.join(IMAGE_DIR_PATH, file.filename)
        with open(path, 'wb') as f:
            f.write(contents)
    finally:
        await file.close()

@payroll_router.post("/add_payroll", response_model=schemas.AddPayrollResponse)
async def add_payroll(payroll_slip: list[UploadFile], staff_id: str = Form(default=''), salary: str = Form(default=''), 
                      net_salary: str = Form(default=''),
                      hourly_salary: str = Form(default=''), bonus_salary: str = Form(default=""),
                      compensation: str = Form(default=''), account_no: str = Form(default=""),
                      hospital_id: str = Form(default=''),db: Session = Depends(get_db)):
    """Function to return final response while adding new payroll details"""
    filenames = []
    if len(payroll_slip) > 0:
      for f in payroll_slip:
          await create_file(f)
          filenames.append(f.filename)
    return controller.add_new_payroll(db, filenames, staff_id, salary,
                              net_salary, hourly_salary, hourly_salary, 
                              bonus_salary,compensation,account_no,hospital_id)


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
async def update_payroll_details(payroll_slip: list[UploadFile], staff_id: str = Form(default=''), salary: str = Form(default=''), 
                      net_salary: str = Form(default=''),
                      hourly_salary: str = Form(default=''), bonus_salary: str = Form(default=""),
                      compensation: str = Form(default=''), account_no: str = Form(default=""),
                      hospital_id: str = Form(default=''),payroll_id: str = Form(default=''),db: Session = Depends(get_db)):
    """Function to update particular bill details"""
    filenames = []
    if len(payroll_slip) > 0:
      for f in payroll_slip:
          await create_file(f)
          filenames.append(f.filename)
    return controller.update_payroll_details(db, filenames, staff_id, salary,
                              net_salary, hourly_salary, hourly_salary, 
                              bonus_salary,compensation,account_no,hospital_id,payroll_id)
