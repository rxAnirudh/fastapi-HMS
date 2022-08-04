"""Main file of our project"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from patient_report.app.api.patient_report_route import patient_report_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=patient_report_router,prefix="/patient_report")

if __name__ == "__main__":
    uvicorn.run(app)
