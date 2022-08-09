"""Controller file for writing db queries for department table"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from fastapi import HTTPException
from response import Response as ResponseData
from models import models,schemas


def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_department(database: Session, department: schemas.DepartmentBase):
    """Function to return query based data while new department creation api"""
    db_department = models.Department(**department.__dict__)
    database.add(db_department)
    database.commit()
    database.refresh(db_department)
    return ResponseData.success(db_department.__dict__,'New Department added successfully')


def get_department_by_id(database: Session, id : Optional[int] = None):
    """Function to get department details by id"""
    db_department = database.query(models.Department).filter(models.Department.id == id).first()
    if db_department is None:
        return ResponseData.success([],'Department id is invalid')
    db_department_details = database.query(models.Department).filter(models.Department.id == id).first()
    return ResponseData.success(db_department_details.__dict__,'Department details fetched successfully')


def delete_department_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all department details if needed"""
    db_department = database.query(models.Department).filter(models.Department.id == id).first()
    if id is None:
        database.query(models.Department).delete()
        database.commit()
        return ResponseData.success([],'All Department details deleted successfully')
    database.query(models.Department).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],'Department details deleted successfully')


def update_department_details(database: Session, department: schemas.AddNewDepartment):
    """Function to update department details"""
    data = database.query(models.Department).filter(models.Department.id == department.id).all()
    dict1 = data[0]
    if department.dict()["name"] is not None :
        dict1.__dict__["name"] = department.dict()["name"]
    if department.dict()["head_id"] is not None :
        dict1.__dict__["head_id"] = department.dict()["head_id"]
    database.query(models.Department).filter(models.Department.id == department.id).update(
    {
        models.Department.id : department.id,
        models.Department.name : department.name,
        models.Department.head_id : department.head_id,
    })
    database.flush()
    database.commit()
    return ResponseData.success([],'Department details Updated successfully')
