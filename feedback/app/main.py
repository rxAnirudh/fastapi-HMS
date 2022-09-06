"""Main file of our project"""
import sys,os
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from feedback.app.api.feedback_route import feedback_router
sys.path.append(os.getcwd())

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router=feedback_router,prefix="/feedback")

if __name__ == "__main__":
    uvicorn.run(app)
