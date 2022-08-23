"""Controller file for writing db queries for affiliation table"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from fastapi import HTTPException
from response import Response as ResponseData
from models import models,schemas


def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_affiliation(database: Session, affiliation: schemas.AffiliationBase):
    """Function to return query based data while new affiliation creation api"""
    db_affiliation = models.Affiliation(**affiliation.__dict__)
    database.add(db_affiliation)
    database.commit()
    database.refresh(db_affiliation)
    return ResponseData.success(db_affiliation.__dict__,'New Affiliation added successfully')


def get_affiliation_by_id(database: Session, id : Optional[int] = None):
    """Function to get affiliation details by id"""
    db_affiliation = database.query(models.Affiliation).filter(models.Affiliation.id == id).first()
    if db_affiliation is None:
        return ResponseData.success([],'Affiliation id is invalid')
    db_affiliation_details = database.query(models.Affiliation).filter(models.Affiliation.id == id).first()
    return ResponseData.success(db_affiliation_details.__dict__,'Affiliation details fetched successfully')


def delete_affiliation_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all affiliation details if needed"""
    db_affiliation = database.query(models.Affiliation).filter(models.Affiliation.id == id).first()
    if id is None:
        database.query(models.Affiliation).delete()
        database.commit()
        return ResponseData.success([],'All Affiliation details deleted successfully')
    database.query(models.Affiliation).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],'Affiliation details deleted successfully')


def update_affiliation_details(database: Session, affiliation: schemas.AddNewAffiliation):
    """Function to update affiliation details"""
    data = database.query(models.Affiliation).filter(models.Affiliation.id == affiliation.id).all()
    dict1 = data[0]
    if affiliation.dict()["staff_id"] is not None :
        dict1.__dict__["staff_id"] = affiliation.dict()["staff_id"]
    if affiliation.dict()["department_id"] is not None :
        dict1.__dict__["department_id"] = affiliation.dict()["department_id"]
    if affiliation.dict()["primaryaffiliation"] is not None :
        dict1.__dict__["primaryaffiliation"] = affiliation.dict()["primaryaffiliation"]
    database.query(models.Affiliation).filter(models.Affiliation.id == affiliation.id).update(
    {
        models.Affiliation.id : affiliation.id,
        models.Affiliation.staff_id : affiliation.staff_id,
        models.Affiliation.department_id : affiliation.department_id,
        models.Affiliation.primaryaffiliation : affiliation.primaryaffiliation,
    })
    database.flush()
    database.commit()
    return ResponseData.success([],'Affiliation details Updated successfully')
