import uvicorn
from fastapi import FastAPI
from db import Base,engine
from demo.app.api.demo_route import demo_router


Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(router=demo_router,prefix='/demo')

if __name__ == '__main__':
    uvicorn.run(app)