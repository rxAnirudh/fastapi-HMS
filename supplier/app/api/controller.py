import sys

from fastapi import HTTPException
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
"""Controller file for writing db queries"""
from typing import Optional
import sys
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from supplier.app.error_handling import Error


# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)


def add_new_supplier(database: Session, supplier: schemas.SupplierBase):
    """Function to return query based data while creating new supplier creation api"""
    for key,value in supplier.dict().items():
        if key == "company" or key == "contact_number" or key == "address":
            is_error = Error.if_param_is_null_or_empty(supplier.dict()[key],key)
            if is_error:
                return ResponseData.success_without_data(f"{key} cannot be empty")
    db_supplier = models.Supplier(**supplier.__dict__)
    database.add(db_supplier)
    database.commit()
    database.refresh(db_supplier)
    return ResponseData.success(db_supplier.__dict__,"New Supplier added successfully")

def get_supplier_by_id(database: Session, id : Optional[int] = None):
    """Function to get room details based on room id generated while adding new supplier"""
    db_supplier = database.query(models.Supplier).filter(models.Supplier.id == id).first()
    if db_supplier is None:
        return ResponseData.success([],"Supplier id is invalid")
    db_supplier_details = database.query(models.Supplier).filter(models.Supplier.id == id).first()
    return ResponseData.success(db_supplier_details.__dict__,"Supplier details fetched successfully")

def delete_supplier_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all Supplier details if needed"""
    if id is None:
        database.query(models.Supplier).delete()
        database.commit()
        return ResponseData.success([],"All Supplier details deleted successfully")
    database.query(models.Supplier).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Supplier details deleted successfully")

def update_supplier_details(database: Session, supplier: schemas.AddNewSupplier):
    """Function to update Supplier details"""
    data = database.query(models.Supplier).filter(models.Supplier.id == supplier.id).all()
    dict1 = data[0]
    if supplier.dict()["company"] is not None :
        dict1.__dict__["company"] = supplier.dict()["company"]
    if supplier.dict()["contact_number"] is not None :
        dict1.__dict__["contact_number"] = supplier.dict()["contact_number"]
    if supplier.dict()["email_id"] is not None :
        dict1.__dict__["email_id"] = supplier.dict()["email_id"]
    if supplier.dict()["address"] is not None :
        dict1.__dict__["address"] = supplier.dict()["address"]
    database.query(models.Supplier).filter(models.Supplier.id == supplier.id).update({ models.Supplier.id : supplier.id,
        models.Supplier.company: dict1.__dict__["company"],
        models.Supplier.contact_number : dict1.__dict__["contact_number"],
        models.Supplier.email_id : dict1.__dict__["email_id"],
        models.Supplier.address : dict1.__dict__["address"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Supplier details updated successfully")

