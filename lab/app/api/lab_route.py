"""File for patient route"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from lab.app.models import schemas
from db import get_db

from api import controller

lab_router = APIRouter()


@lab_router.post("/add_lab", response_model=schemas.AddLabResponse)
def add_bill(lab: schemas.LabBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new lab details"""
    return controller.add_new_lab(database,lab)


@lab_router.post("/get_lab_details")
def get_lab_details(labid: schemas.LabId, database: Session = Depends(get_db)):
    """Function to return lab details
    (specific and all lab data can be fetched)"""
    return controller.get_lab_by_id(database, id = labid.id)


@lab_router.post("/delete_lab_details")
def delete_lab_details(labid: schemas.LabId, database: Session = Depends(get_db)):
    """Function to return lab details
    (specific and all lab data can be fetched)"""
    return controller.delete_lab_details(database, id = labid.id)


@lab_router.post("/update_lab_details")
def update_lab_details(lab_details: schemas.AddNewLab, database: Session = Depends(get_db)):
    """Function to update particular lab details"""
    return controller.update_lab_details(database, lab = lab_details)
