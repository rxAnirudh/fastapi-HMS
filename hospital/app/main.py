"""Main file of our project"""
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from api import hospital_route
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=hospital_route.hospital_router,prefix="/hospital")

if __name__ == "__main__":
    print("called")
    uvicorn.run(app)
    add_pagination(app)


