"""Main file of our project"""
from fastapi import FastAPI
import uvicorn
from db import Base,engine
from api import hospital_route
from fastapi.testclient import TestClient

Base.metadata.create_all(engine)

app = FastAPI()

client = TestClient(app)

app.include_router(router=hospital_route.hospital_router,prefix="/hospital")

if __name__ == "__main__":
    print("called")
    uvicorn.run(app)

def test_valid_id():
    response = client.post("/fruit/1")
    assert response.status_code == 200
    assert response.json() == {"fruit": "apple"}