"""File for patient route"""
import sys,os
from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from authentication import Authentication
from db import get_db
from api import controller
from feedback.app.models import schemas
sys.path.append(os.getcwd())

feedback_router = APIRouter()


@feedback_router.post("/add_feedback", response_model=schemas.AddFeedbackResponse)
def add_feedback(request:Request,feedback: schemas.FeedbackBase, database: Session = Depends(get_db)):
    """Function to return final response while adding new feedback details"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.add_new_feedback(database,feedback)


@feedback_router.post("/get_feedback_details")
def get_payroll_details(request:Request,feedbackid: schemas.FeedbackId, database: Session = Depends(get_db)):
    """Function to return feedback details
    (specific and all feedback data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.get_feedback_by_id(database, id = feedbackid.id)


@feedback_router.post("/delete_feedback_details")
def delete_feedback_details(request:Request,feedbackid: schemas.FeedbackId, database: Session = Depends(get_db)):
    """Function to return feedback details
    (specific and all feedback data can be fetched)"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.delete_feedback_details(database, id = feedbackid.id)


@feedback_router.post("/update_feedback_details")
def update_feedback_details(request:Request,feedback_details: schemas.AddNewFeedback, database: Session = Depends(get_db)):
    """Function to update particular feedback details"""
    Authentication().authenticate(request.headers.get('Authorization'),database)
    return controller.update_feedback_details(database, feedback = feedback_details)
