"""Main file of our project"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import FastAPI
import uvicorn
from appointment.app.db import Base,appointment_engine
from fastapi.staticfiles import StaticFiles #new
from appointment.app.api.appointment_route import appointment_router
Base.metadata.create_all(appointment_engine)

app = FastAPI()

def configure_static(app):  #new
    app.mount("/appointment_files", StaticFiles(directory='appointment_files'), name="appointment_files")

configure_static(app)

app.include_router(router=appointment_router,prefix="/appointment")

# app.include_router(router=doctor_route.doctor_router,prefix="/doctor")

if __name__ == "__main__":
    uvicorn.run(app)
