"""File for patient route"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import Depends, APIRouter,Request
from sqlalchemy.orm import Session
from medicine.app.models import schemas
from medicine.app.db import get_db

from medicine.app.api import controller

medicine_router = APIRouter()


@medicine_router.post("/add_medicine")
async def add_medicine(request:Request, database: Session = Depends(get_db)):
    """Function to return final response while adding new medicine details"""
    request_json = await request.json()
    return controller.add_new_medicine(database,request_json)


@medicine_router.post("/get_medicine_details")
async def get_medicine_details(request:Request, database: Session = Depends(get_db)):
    """Function to return medicine details
    (specific and all medicine data can be fetched)"""
    request_json = await request.json()
    id = ""
    if request_json["id"] != "":
        id = request_json["id"]
    return controller.get_medicine_by_id(database, id)

@medicine_router.get("/get_medicine_by_pagination")
async def get_medicine_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to get medicine details through pagination concept"""
    return controller.get_medicine_by_pagination(database,page,size)

@medicine_router.post("/delete_medicine_details")
def delete_medicine_details(medicineid: schemas.MedicineId, database: Session = Depends(get_db)):
    """Function to return medicine details
    (specific and all medicine data can be fetched)"""
    return controller.delete_medicine_details(database, id = medicineid.id)


@medicine_router.post("/update_medicine_details")
def update_medicine_details(medicine_details: schemas.AddNewMedicine, database: Session = Depends(get_db)):
    """Function to update particular medicine details"""
    return controller.update_medicine_details(database, medicine = medicine_details)
