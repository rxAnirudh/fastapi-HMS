"""Main file of our project"""
import os
import sys
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from doctor.app.db import Base as doctorBase,doctor_engine
from appointment.app.db import Base as appointmentBase,appointment_engine
from patient.app.db import Base as patientBase,patient_engine
from fastapi.staticfiles import StaticFiles #new
from appointment.app.api.appointment_route import appointment_router
from doctor.app.api.doctor_route import doctor_router
from patient.app.api.patient_route import patient_router
from fastapi.middleware.cors import CORSMiddleware

doctorBase.metadata.create_all(doctor_engine)
appointmentBase.metadata.create_all(appointment_engine)
patientBase.metadata.create_all(patient_engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def configure_static(app):  #new
    app.mount("/appointment/app/appointment_files", StaticFiles(directory=f'{os.getcwd()}/appointment/app/appointment_files'), name="appointment_files")
    app.mount("/patient/app/patient_images", StaticFiles(directory=f'{os.getcwd()}/patient/app/patient_images'), name="patient_images")
    app.mount("/patient/app/patient_profile_pic_files", StaticFiles(directory=f"{os.getcwd()}/patient/app/patient_profile_pic_files"), name="patient_profile_pic_files")
    app.mount("/doctor/app/doctor_images", StaticFiles(directory=f"{os.getcwd()}/doctor/app/doctor_images"), name="doctor_images")

configure_static(app)

app.include_router(router=doctor_router,prefix="/doctor")
app.include_router(router=appointment_router,prefix="/appointment")
app.include_router(router=patient_router,prefix="/patient")

if __name__ == "__main__":
    uvicorn.run(app)
