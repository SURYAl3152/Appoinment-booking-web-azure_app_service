from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel  
from models import Appointment, AppointmentCreate, AppointmentOut
from database import SessionLocal, engine, Base
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# ✅ Only declare app ONCE
app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class AppointmentCreate(BaseModel):
    name: str
    email: str
    appointment_date: datetime

class AppointmentOut(BaseModel):
    id: int
    name: str
    email: str
    appointment_date: datetime

    class Config:
        orm_mode = True

# Routes
@app.post("/appointments/", response_model=AppointmentOut)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.get("/appointments/", response_model=List[AppointmentOut])
def read_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}
