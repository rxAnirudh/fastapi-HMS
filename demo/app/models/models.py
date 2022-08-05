from sqlalchemy import Column, Integer,  String
from db import Base

class Demo(Base):
    __tablename__ = 'demo'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    doctor_charge = Column(String, index=True)
    medicine_charge = Column(String, index=True)
    room_charge = Column(String, index=True)
    operation_charge = Column(String, index=True)
    no_of_days = Column(String, index=True)
    nursing_charge = Column(String, index=True)
    lab_charge = Column(String,index = True)
    insurance_number = Column(String, index=True)
    total_bill = Column(String, index=True)
    bill_date = Column(String,index=False)
    hospital_id = Column(String, index=True)

DATABASE_URL = 'postgresql://anirudh.chawla:123@localhost/demo'