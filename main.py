from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
import os

from database import SessionLocal, engine, Base
from models import Appointment

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve homepage
@app.get("/", response_class=HTMLResponse)
def serve_home():
    return FileResponse(os.path.join("static", "index.html"))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
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

@app.put("/appointments/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)

    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}
