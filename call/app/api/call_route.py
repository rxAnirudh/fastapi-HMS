"""File for call route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from api import controller
from models import schemas


call_router = APIRouter()


@call_router.post('/create_call', response_model=schemas.Response)
def create_call(call: schemas.CallBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new call details"""
    return controller.add_new_call(database,call)


@call_router.post('/get_call')
def get_call(callid: schemas.CallId, database: Session = Depends(get_db)):
    """Function to return call details (specific and all call data can be fetched)"""
    return controller.get_call_by_id(database, id = callid.id)


@call_router.post('/delete_call')
def delete_call(callid: schemas.CallId, database: Session = Depends(get_db)):
    """Function to return call details (specific and all call data can be deleted)"""
    return controller.delete_call_details(database, id = callid.id)


@call_router.post('/update_call')
def update_call(call_details: schemas.AddNewCall, database: Session = Depends(get_db)):
    """Function to update particular call details"""
    return controller.update_call_details(database, call = call_details)


