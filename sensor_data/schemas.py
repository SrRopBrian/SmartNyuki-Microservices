from pydantic import BaseModel
from datetime import datetime

class SensorReadingCreate(BaseModel):
    hive_id: str
    temperature: float
    humidity: float
    weight: float
    sound_level: float

class SensorReadingOut(SensorReadingCreate):
    timestamp: datetime

    class Config:
        from_attributes = True
