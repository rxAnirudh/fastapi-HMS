"""Main file of our project"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from patient_report.app.api.patient_report_route import patient_report_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=patient_report_router,prefix="/patient_report")

if __name__ == "__main__":
    uvicorn.run(app)
