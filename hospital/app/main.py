"""Main file of our project"""
from fastapi import FastAPI
import uvicorn
from app.db import Base,engine
from app.api import hospital_route

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(prefix="/hospital", router=hospital_route)

if __name__ == "__main__":
    print("called")
    uvicorn.run(app)
