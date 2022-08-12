"""File for affiliation route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from api import controller
from models import schemas


affiliation_router = APIRouter()


@affiliation_router.post('/create_affiliation', response_model=schemas.Response)
def create_affiliation(affiliation: schemas.AffiliationBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new affiliation details"""
    return controller.add_new_affiliation(database,affiliation)


@affiliation_router.post('/get_affiliation')
def get_affiliation(affiliationid: schemas.AffiliationId, database: Session = Depends(get_db)):
    """Function to return affiliation details (specific and all affiliation data can be fetched)"""
    return controller.get_affiliation_by_id(database, id = affiliationid.id)


@affiliation_router.post('/delete_affiliation')
def delete_affiliation(affiliationid: schemas.AffiliationId, database: Session = Depends(get_db)):
    """Function to return affiliation details (specific and all affiliation data can be deleted)"""
    return controller.delete_affiliation_details(database, id = affiliationid.id)


@affiliation_router.post('/update_affiliation')
def update_affiliation(affiliation_details: schemas.AddNewAffiliation, database: Session = Depends(get_db)):
    """Function to update particular affiliation details"""
    return controller.update_affiliation_details(database, affiliation = affiliation_details)


