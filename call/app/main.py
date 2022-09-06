import sys,os
sys.path.append(os.getcwd())
import uvicorn
from fastapi import FastAPI
from db import Base,engine
from call.app.api.call_route import call_router


Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router=call_router,prefix='/call')

if __name__ == '__main__':
    uvicorn.run(app)