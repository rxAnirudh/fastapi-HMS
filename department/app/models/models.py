from sqlalchemy import Column, Integer,  String
from db import Base

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    head_id = Column(String, index=True)

DATABASE_URL = 'postgresql://anirudh.chawla:123@localhost/department'