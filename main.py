"""Main file of our project"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import FastAPI
import uvicorn
from appointment.app.db import Base as appointmentBase,appointment_engine
from doctor.app.db import Base as doctorBase,doctor_engine
from patient.app.db import Base as patientBase,patient_engine
from fastapi.staticfiles import StaticFiles #new
from appointment.app.api.appointment_route import appointment_router
from doctor.app.api.doctor_route import doctor_router
from patient.app.api.patient_route import patient_router
from fastapi.middleware.cors import CORSMiddleware

appointmentBase.metadata.create_all(appointment_engine)
doctorBase.metadata.create_all(doctor_engine)
patientBase.metadata.create_all(patient_engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def configure_static(app):  #new
    app.mount("/appointment_files", StaticFiles(directory='/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/appointment/app/appointment_files'), name="appointment_files")
    app.mount("/patient_images", StaticFiles(directory='/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/patient/app/patient_images'), name="patient_images")
    app.mount("/patient_images", StaticFiles(directory="/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi/patient/app/patient_images"), name="patient_images")

configure_static(app)

app.include_router(router=appointment_router,prefix="/appointment")

app.include_router(router=doctor_router,prefix="/doctor")

app.include_router(router=patient_router,prefix="/patient")

if __name__ == "__main__":
    uvicorn.run(app)
