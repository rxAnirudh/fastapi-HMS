"""Main file of our project"""
import sys,os
import uvicorn
from fastapi import FastAPI
from db import Base,engine
from insurance.app.api.insurance_route import insurance_router
sys.path.append(os.getcwd())

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=insurance_router,prefix="/insurance")

if __name__ == "__main__":
    uvicorn.run(app)
