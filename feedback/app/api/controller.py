import sys,os

from fastapi import HTTPException
sys.path.append(os.getcwd())
"""Controller file for writing db queries"""
from typing import Optional
from sqlalchemy.orm import Session
from models import models,schemas
from response import Response as ResponseData
from hospital.app.api.controller import check_if_hospital_id_is_valid
from staff.app.api.controller import check_if_staff_id_is_valid
from patient.app.api.controller import check_if_patient_id_is_valid



# Python code to merge dict using update() method
def Merge(dict1, dict2):
    """Function to merge dict using update method"""
    return dict2.update(dict1)

def add_new_feedback(database: Session, feedback: schemas.FeedbackBase):
    """Function to add new feedback of staff working in hospital"""
    if not check_if_hospital_id_is_valid(database,feedback.dict()["hospital_id"]):
        raise HTTPException(status_code=400, detail="Hospital id is invalid")
    if not check_if_staff_id_is_valid(database,feedback.dict()["to_staff_id"]):
        raise HTTPException(status_code=400, detail="Staff id is invalid")
    if not check_if_patient_id_is_valid(database,feedback.dict()["from_patient_id"]):
        raise HTTPException(status_code=400, detail="Patient id is invalid")
    db_feedback = models.Feedback(**feedback.__dict__)
    database.add(db_feedback)
    database.commit()
    database.refresh(db_feedback)
    return ResponseData.success(db_feedback.__dict__,"Feedback for this staff added successfully")

def get_feedback_by_id(database: Session, id : Optional[int] = None):
    """Function to get feedback details by id"""
    db_feedback = database.query(models.Feedback).filter(models.Feedback.id == id).first()
    if db_feedback is None:
        return ResponseData.success([],"Feedback with this id does not exists")
    return ResponseData.success(db_feedback.__dict__,"Feedback details fetched successfully")

def delete_feedback_details(database: Session, id : Optional[int] = None):
    """Function to delete single or all feedback details if needed"""
    if id is None:
        database.query(models.Feedback).delete()
        database.commit()
        return ResponseData.success([],"All Feedback details deleted successfully")
    database.query(models.Feedback).filter_by(id = id).delete()
    database.commit()
    return ResponseData.success([],"Feedback details deleted successfully")

def update_feedback_details(database: Session, feedback: schemas.AddNewFeedback):
    """Function to update feedback details"""
    data = database.query(models.Feedback).filter(models.Feedback.id == feedback.id).all()
    dict1 = data[0]
    if feedback.dict()["from_patient_id"] is not None :
        dict1.__dict__["from_patient_id"] = feedback.dict()["from_patient_id"]
    if feedback.dict()["to_staff_id"] is not None :
        dict1.__dict__["to_staff_id"] = feedback.dict()["to_staff_id"]
    if feedback.dict()["comment"] is not None :
        dict1.__dict__["comment"] = feedback.dict()["comment"]
    if feedback.dict()["rating"] is not None :
        dict1.__dict__["rating"] = feedback.dict()["rating"]
    if feedback.dict()["created_on"] is not None :
        dict1.__dict__["created_on"] = feedback.dict()["created_on"]
    if feedback.dict()["updated_on"] is not None :
        dict1.__dict__["updated_on"] = feedback.dict()["updated_on"]
    if feedback.dict()["hospital_id"] is not None :
        dict1.__dict__["hospital_id"] = feedback.dict()["hospital_id"]
    database.query(models.Feedback).filter(models.Feedback.id == feedback.id).update({ models.Feedback.id : feedback.id,
        models.Feedback.from_patient_id: dict1.__dict__["from_patient_id"],
        models.Feedback.to_staff_id : dict1.__dict__["to_staff_id"],
        models.Feedback.comment : dict1.__dict__["comment"],
        models.Feedback.rating : dict1.__dict__["rating"],
        models.Feedback.created_on : dict1.__dict__["created_on"],
        models.Feedback.updated_on : dict1.__dict__["updated_on"],
        models.Feedback.hospital_id : dict1.__dict__["hospital_id"],
    })
    database.flush()
    database.commit()
    return ResponseData.success(dict1.__dict__,"Feedback details updated successfully")
