from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    hive_id = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    weight = Column(Float)
    sound_level = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
