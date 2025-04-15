from sqlalchemy.orm import Session
from models import SensorReading
from schemas import SensorReadingCreate

def create_reading(db: Session, reading: SensorReadingCreate):
    db_reading = SensorReading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def get_latest_readings(db: Session, hive_id: str, limit: int = 5):
    return (
        db.query(SensorReading)
        .filter(SensorReading.hive_id == hive_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(limit)
        .all()
    )
