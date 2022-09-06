"""Main file of our project"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from lab.app.api.lab_route import lab_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=lab_router,prefix="/lab")

if __name__ == "__main__":
    uvicorn.run(app)
