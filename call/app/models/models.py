from sqlalchemy import Column, Integer,  String
from db import Base

class Call(Base):
    __tablename__ = 'call'

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, index=True)
    block_floor_id = Column(String, index=True)
    block_code_id = Column(String, index=True)
    on_call_start = Column(String, index=True)
    on_call_end = Column(String, index=True)

DATABASE_URL = 'postgresql://anirudh.chawla:123@localhost/call'