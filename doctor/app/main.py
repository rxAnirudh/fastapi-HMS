"""Main file of our project"""
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from api import doctor_route

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=doctor_route.doctor_router,prefix="/doctor")

if __name__ == "__main__":
    uvicorn.run(app)
