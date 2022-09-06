"""Main file of our project"""
import sys,os
sys.path.append(os.getcwd())
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from room.app.api.room_route import room_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=room_router,prefix="/room")

if __name__ == "__main__":
    uvicorn.run(app)
