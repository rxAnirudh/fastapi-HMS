"""File for patient route"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from bill.app.models import schemas
from db import get_db

from api import controller

bill_router = APIRouter()


@bill_router.post("/add_bill", response_model=schemas.AddBillResponse)
def add_bill(bill: schemas.BillBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new bill details"""
    return controller.add_new_bill(database,bill)


@bill_router.post("/get_bill_details")
def get_bill_details(billid: schemas.BillId, database: Session = Depends(get_db)):
    """Function to return bill details
    (specific and all bill data can be fetched)"""
    return controller.get_bill_by_id(database, id = billid.id)


@bill_router.post("/delete_bill_details")
def delete_bill_details(billid: schemas.BillId, database: Session = Depends(get_db)):
    """Function to return bill details
    (specific and all bill data can be fetched)"""
    return controller.delete_bill_details(database, id = billid.id)


@bill_router.post("/update_bill_details")
def update_bill_details(bill_details: schemas.AddNewBill, database: Session = Depends(get_db)):
    """Function to update particular bill details"""
    return controller.update_bill_details(database, bill = bill_details)
