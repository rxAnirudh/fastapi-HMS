"""File for patient route"""
import os
import sys

from authentication import Authentication
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends, File, Form,  HTTPException, APIRouter,Request, UploadFile
from sqlalchemy.orm import Session
from bill.app.models import schemas
from db import get_db
from bunch import bunchify
from api import controller
from datetime import datetime

bill_router = APIRouter()

IMAGE_DIR_PATH = "/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/bill/bill_images"

async def create_file(file=File(None)):
    try:
        contents = await file.read()
        path = os.path.join(IMAGE_DIR_PATH, file.filename)
        with open(path, 'wb') as f:
            f.write(contents)
    finally:
        await file.close()


@bill_router.post("/add_bill", response_model=schemas.AddBillResponse)
async def add_bill(request:Request,bill_photo: list[UploadFile], patient_id: str = Form(default=''), doctor_charge: str = Form(default=''), medicine_charge: str = Form(default=''),
                      room_charge: str = Form(default=''), operation_charge: str = Form(default=""),
                      nursing_charge: str = Form(default=''), lab_charge: str = Form(default=""),
                      insurance_number: str = Form(default=''), total_bill: str = Form(default=""),
                      bill_date: str = Form(default=str(datetime.utcnow())), hospital_id: str = Form(default=""),
                       no_of_days: str = Form(default=''), db: Session = Depends(get_db)):
    """Function to return final response while adding new bill details"""
    Authentication().authenticate(request.headers.get('Authorization'),db)
    filenames = []
    if len(bill_photo) > 0:
      for f in bill_photo:
          await create_file(f)
          filenames.append(f.filename)
    return controller.add_new_bill(db, filenames, patient_id, doctor_charge,
                              medicine_charge, room_charge, operation_charge, 
                              nursing_charge,lab_charge,insurance_number,
                              total_bill,bill_date,hospital_id,no_of_days)


@bill_router.post("/get_bill_details")
def get_bill_details(request:Request,billid: schemas.BillId, database: Session = Depends(get_db)):
    """Function to return bill details
    (specific and all bill data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.get_bill_by_id(database, id = billid.id)

@bill_router.get("/get_bill_by_pagination")
async def get_bill_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to update particular bill details"""
    return controller.get_bill_by_pagination(database,page,size)

@bill_router.post("/delete_bill_details")
def delete_bill_details(request:Request,billid: schemas.BillId, database: Session = Depends(get_db)):
    """Function to return bill details
    (specific and all bill data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.delete_bill_details(database, id = billid.id)


@bill_router.post("/update_bill_details")
async def update_bill_details(request:Request,bill_photo: list[UploadFile], patient_id: str = Form(default=''), doctor_charge: str = Form(default=''), medicine_charge: str = Form(default=''),
                      room_charge: str = Form(default=''), operation_charge: str = Form(default=""),
                      nursing_charge: str = Form(default=''), lab_charge: str = Form(default=""),
                      insurance_number: str = Form(default=''), total_bill: str = Form(default=""),
                      bill_date: str = Form(default=str(datetime.utcnow())), hospital_id: str = Form(default=""),
                       no_of_days: str = Form(default=''),bill_id: str = Form(default=''), db: Session = Depends(get_db)):
    """Function to update particular bill details"""
    Authentication().authenticate(request.headers.get('Authorization'),db)
    filenames = []
    if len(bill_photo) > 0:
      for f in bill_photo:
          await create_file(f)
          filenames.append(f.filename)
    return controller.update_bill_details(db, filenames, patient_id, doctor_charge,
                              medicine_charge, room_charge, operation_charge, 
                              nursing_charge,lab_charge,insurance_number,
                              total_bill,bill_date,hospital_id,no_of_days,bill_id)
