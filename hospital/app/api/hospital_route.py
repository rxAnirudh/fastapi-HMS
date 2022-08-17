"""File for hospital route"""
from fastapi import Depends, APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import schemas
from db import get_db
from api import controller

hospital_router = APIRouter()

app = FastAPI()

@hospital_router.post("/create_hospital")
def create_hospital(hospital: schemas.HospitalBase, database: Session = Depends(get_db)):
    """Function to return final response while creating new_hospital creation api"""
    # db_hospital = controller.get_hospital(database, contact_number=hospital.contact_number)
    # if db_hospital:
    #     raise HTTPException(status_code=400, detail="Hospital already registered with same contact number")
    return controller.create_hospital(database,hospital)


@hospital_router.post("/get_hospital")
def get_hospital(hospitalid: schemas.HospitalId, database: Session = Depends(get_db)):
    """Function to return hospital details
    (specific and all hospitals data can be fetched)"""
    return controller.get_hospital_by_id(database, id = hospitalid.id)

@hospital_router.post("/search_hospital_by_name")
def search_hospital_by_name(hospitalname: schemas.HospitalName, database: Session = Depends(get_db)):
    """Function to return hospital details
    (specific and all hospitals data can be fetched)"""
    return controller.search_hospital_by_name(database, hospital_name = hospitalname.name)

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@hospital_router.get("/get_hospital_by_pagination")
async def get_hospital_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to update particular hospital details"""
    return controller.get_hospital_by_pagination(database,page,size)

@hospital_router.post("/delete_hospital")
def delete_hospital(hospitalid: schemas.HospitalId, database: Session = Depends(get_db)):
    """Function to return hospital details
    (specific and all hospitals data can be fetched)"""
    return controller.delete_hospital(database, id = hospitalid.id)


@hospital_router.post("/update_hospital")
def update_hospital(hospital_details: schemas.HospitalCreate, database: Session = Depends(get_db)):
    """Function to update particular hospital details"""
    return controller.update_hospital(database, hospital = hospital_details)
