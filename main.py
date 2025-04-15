from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from models import Appointment, AppointmentCreate, AppointmentOut
from database import SessionLocal, engine, Base
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os

# ✅ Initialize app
app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Mount static directory if needed
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Serve index.html at root
@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    try:
        with open("index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

# ✅ Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Pydantic schemas
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

# ✅ API routes
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
