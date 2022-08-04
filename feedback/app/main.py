"""Main file of our project"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from feedback.app.api.feedback_route import feedback_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=feedback_router,prefix="/feedback")

if __name__ == "__main__":
    uvicorn.run(app)
