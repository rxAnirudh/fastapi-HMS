"""File for department route"""
from fastapi import Depends,  HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from api import controller
from models import schemas


department_router = APIRouter()


@department_router.post('/create_department', response_model=schemas.Response)
def create_department(department: schemas.DepartmentBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new department details"""
    return controller.add_new_department(database,department)


@department_router.post('/get_department')
def get_department(departmentid: schemas.DepartmentId, database: Session = Depends(get_db)):
    """Function to return department details (specific and all department data can be fetched)"""
    return controller.get_department_by_id(database, id = departmentid.id)

@department_router.get("/get_department_by_pagination")
async def get_department_by_pagination(database: Session = Depends(get_db),page: int = 0, size: int = 5):
    """Function to update particular department details"""
    return controller.get_department_by_pagination(database,page,size)

@department_router.post('/delete_department')
def delete_department(departmentid: schemas.DepartmentId, database: Session = Depends(get_db)):
    """Function to return department details (specific and all department data can be deleted)"""
    return controller.delete_department_details(database, id = departmentid.id)


@department_router.post('/update_department')
def update_department(department_details: schemas.AddNewDepartment, database: Session = Depends(get_db)):
    """Function to update particular department details"""
    return controller.update_department_details(database, department = department_details)


