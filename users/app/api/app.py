"""
Uvicorn for running app
"""
import uvicorn

"""
Base package for all API
"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    """
    Top level API for check
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app)
    