"""Main file of our project"""
import sys
from fastapi import FastAPI
import uvicorn
from db import Base,engine
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
from bill.app.api.bill_route import bill_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=bill_router,prefix="/bill")

if __name__ == "__main__":
    uvicorn.run(app)

