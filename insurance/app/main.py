"""Main file of our project"""
import sys
import uvicorn
from fastapi import FastAPI
from db import Base,engine
from insurance.app.api.insurance_route import insurance_router
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=insurance_router,prefix="/insurance")

if __name__ == "__main__":
    uvicorn.run(app)
