"""File for hospital route"""
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from models import schemas
from db import get_db

from api import controller

staff_router = APIRouter()


@staff_router.post("/add_staff", response_model=schemas.AddStaffResponse)
def add_staff(staff: schemas.StaffBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new staff details"""
    db_staff = controller.get_staff(database, contact_number=staff.contact_number)
    if db_staff:
        raise HTTPException(status_code=400, detail="Staff already registered with same contact number")
    return controller.add_new_staff(database,staff)


@staff_router.post("/get_staff_details")
def get_staff(staffid: schemas.StaffId, database: Session = Depends(get_db)):
    """Function to return staff details
    (specific and all staff data can be fetched)"""
    return controller.get_staff_by_id(database, id = staffid.id)

@staff_router.get("/get_staff_by_pagination")
async def get_staff_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to get staff details through pagination concept"""
    return controller.get_staff_by_pagination(database,page,size)

@staff_router.post("/delete_staff_details")
def delete_staff(staffid: schemas.StaffId, database: Session = Depends(get_db)):
    """Function to return staff details
    (specific and all staff data can be deleted)"""
    return controller.delete_staff_details(database, id = staffid.id)


@staff_router.post("/update_staff_details")
def update_staff_details(staff_details: schemas.AddNewStaff, database: Session = Depends(get_db)):
    """Function to update particular staff details"""
    return controller.update_staff_details(database, staff = staff_details)
