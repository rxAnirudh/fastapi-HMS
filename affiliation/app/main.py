import sys
import os
sys.path.append({os.getcwd()})
import uvicorn
from fastapi import FastAPI
from db import Base,engine
from affiliation.app.api.affiliation_route import affiliation_router


Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router=affiliation_router,prefix='/affiliation')

if __name__ == '__main__':
    uvicorn.run(app)