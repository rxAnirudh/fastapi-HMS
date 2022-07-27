"""Main file of our project"""
from fastapi import FastAPI
import uvicorn
from db.database import engine, Base,SessionLocal
from api.hospital.hospital_route import hospital_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(prefix="/hospital", router=hospital_router)

if __name__ == "__main__":
    print("called")
    uvicorn.run(app)
