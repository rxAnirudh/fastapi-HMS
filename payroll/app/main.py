"""Main file of our project"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from payroll.app.api.payroll_route import payroll_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=payroll_router,prefix="/payroll")

if __name__ == "__main__":
    uvicorn.run(app)
