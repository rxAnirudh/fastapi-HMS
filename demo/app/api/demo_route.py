"""File for demo route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from api import controller
from models import schemas


demo_router = APIRouter()


@demo_router.post('/create_demo', response_model=schemas.Response)
def create_demo(demo: schemas.DemoBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new demo details"""
    return controller.add_new_demo(database,demo)


@demo_router.post('/get_demo')
def get_demo(demoid: schemas.DemoId, database: Session = Depends(get_db)):
    """Function to return demo details (specific and all demo data can be fetched)"""
    return controller.get_demo_by_id(database, id = demoid.id)


@demo_router.post('/delete_demo')
def delete_demo(demoid: schemas.DemoId, database: Session = Depends(get_db)):
    """Function to return demo details (specific and all demo data can be deleted)"""
    return controller.delete_demo_details(database, id = demoid.id)


@demo_router.post('/update_demo')
def update_demo(demo_details: schemas.AddNewDemo, database: Session = Depends(get_db)):
    """Function to update particular demo details"""
    return controller.update_demo_details(database, demo = demo_details)


