from sqlalchemy import Column, Integer,  String
from db import Base

class Affiliation(Base):
    __tablename__ = 'affiliation'

    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(String, index=True)
    department_id = Column(String, index=True)
    primaryaffiliation = Column(String, index=True)

DATABASE_URL = 'postgresql://anirudh.chawla:123@localhost/affiliation'