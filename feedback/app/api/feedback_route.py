"""File for patient route"""
import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from db import get_db
from api import controller
from feedback.app.models import schemas
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')

feedback_router = APIRouter()


@feedback_router.post("/add_feedback", response_model=schemas.AddFeedbackResponse)
def add_feedback(feedback: schemas.FeedbackBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new feedback details"""
    return controller.add_new_feedback(database,feedback)


@feedback_router.post("/get_feedback_details")
def get_payroll_details(feedbackid: schemas.FeedbackId, database: Session = Depends(get_db)):
    """Function to return feedback details
    (specific and all feedback data can be fetched)"""
    return controller.get_feedback_by_id(database, id = feedbackid.id)


@feedback_router.post("/delete_feedback_details")
def delete_feedback_details(feedbackid: schemas.FeedbackId, database: Session = Depends(get_db)):
    """Function to return feedback details
    (specific and all feedback data can be fetched)"""
    return controller.delete_feedback_details(database, id = feedbackid.id)


@feedback_router.post("/update_feedback_details")
def update_feedback_details(feedback_details: schemas.AddNewFeedback, database: Session = Depends(get_db)):
    """Function to update particular feedback details"""
    return controller.update_feedback_details(database, feedback = feedback_details)
