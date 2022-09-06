"""Main file of our project"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from patient.app.api.patient_route import patient_router
from fastapi.staticfiles import StaticFiles #new
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def configure_static(app):  #new
    app.mount("/patient_images", StaticFiles(directory="patient_images"), name="patient_images")

configure_static(app)

app.include_router(router=patient_router,prefix="/patient")

if __name__ == "__main__":
    uvicorn.run(app)
