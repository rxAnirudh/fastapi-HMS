"""File for hospital route"""
from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from authentication import Authentication
from models import schemas
from db import get_db

from api import controller

insurance_router = APIRouter()


@insurance_router.post("/add_new_insurance", response_model=schemas.AddInsuranceResponse)
def add_new_insurance(request:Request,insurance: schemas.InsuranceBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new insurance details"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.add_new_insurance(database,insurance)


@insurance_router.post("/get_insurance_details")
def get_insurance_details(request:Request,insuranceid: schemas.InsuranceId, database: Session = Depends(get_db)):
    """Function to return insurance details
    (specific and all insurance data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.get_insurance_details_by_id(database, id = insuranceid.id)


@insurance_router.post("/delete_insurance_details")
def delete_insurance_details(request:Request,staffid: schemas.InsuranceId, database: Session = Depends(get_db)):
    """Function to return insurance details
    (specific and all insurance data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.delete_insurance_details(database, id = staffid.id)


@insurance_router.post("/update_insurance_details")
def update_insurance_details(request:Request,insurance_details: schemas.AddNewInsurance, database: Session = Depends(get_db)):
    """Function to update particular insurance details"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.update_insurance_details(database, insurance = insurance_details)
