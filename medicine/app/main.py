"""Main file of our project"""
from db import Base,engine
import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from fastapi import FastAPI
import uvicorn
from medicine.app.api.medicine_route import medicine_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=medicine_router,prefix="/medicine")

if __name__ == "__main__":
    uvicorn.run(app)
