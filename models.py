from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    appointment_date = Column(DateTime)


class AppointmentCreate(BaseModel):
    name: str
    email: str
    appointment_date: datetime  
    class Config:
        orm_mode = True 


class AppointmentOut(BaseModel):
    id: int
    name: str
    email: str
    appointment_date: datetime

    class Config:
        orm_mode = True


print(AppointmentOut)
