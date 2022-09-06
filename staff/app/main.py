"""Main file of our project"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from staff.app.api.staff_route import staff_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=staff_router,prefix="/staff")

if __name__ == "__main__":
    uvicorn.run(app)
