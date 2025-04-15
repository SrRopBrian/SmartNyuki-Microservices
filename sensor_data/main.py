from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sensor Data Microservice")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/readings/", response_model=schemas.SensorReadingOut)
def add_reading(reading: schemas.SensorReadingCreate, db: Session = Depends(get_db)):
    return crud.create_reading(db, reading)

@app.get("/readings/{hive_id}", response_model=list[schemas.SensorReadingOut])
def get_readings(hive_id: str, db: Session = Depends(get_db)):
    readings = crud.get_latest_readings(db, hive_id)
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found")
    return readings
