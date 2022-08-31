"""Main file of our project"""
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import FastAPI
import uvicorn
from db import Base,doctor_engine
from fastapi.staticfiles import StaticFiles #new
from api import doctor_route

Base.metadata.create_all(doctor_engine)

app = FastAPI()

def configure_static(app):  #new
    app.mount("/doctor_images", StaticFiles(directory="doctor_images"), name="doctor_images")

configure_static(app)

app.include_router(router=doctor_route.doctor_router,prefix="/doctor")



if __name__ == "__main__":
    uvicorn.run(app)
