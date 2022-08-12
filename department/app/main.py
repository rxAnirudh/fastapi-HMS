import sys
sys.path.append('/Users/anirudh.chawla/python_fast_api_projects/hospital-management-fastapi')
import uvicorn
from fastapi import FastAPI
from db import Base,engine
from department.app.api.department_route import department_router


Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router=department_router,prefix='/department')

if __name__ == '__main__':
    uvicorn.run(app)