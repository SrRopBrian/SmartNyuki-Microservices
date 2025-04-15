from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Hive Management Microservice 🐝")

DATABASE_URL = "sqlite:///./hives.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Database Model ---
class Hive(Base):
    __tablename__ = "hives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    status = Column(String, default="Active")


Base.metadata.create_all(bind=engine)


# --- Pydantic Schemas ---
class HiveCreate(BaseModel):
    name: str
    location: str
    status: Optional[str] = "Active"


class HiveOut(HiveCreate):
    id: int

    class Config:
        orm_mode = True


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Routes ---
@app.post("/hives/", response_model=HiveOut)
def create_hive(hive: HiveCreate, db: SessionLocal = next(get_db())):
    db_hive = Hive(**hive.dict())
    db.add(db_hive)
    db.commit()
    db.refresh(db_hive)
    return db_hive


@app.get("/hives/", response_model=List[HiveOut])
def list_hives(db: SessionLocal = next(get_db())):
    return db.query(Hive).all()


@app.get("/hives/{hive_id}", response_model=HiveOut)
def get_hive(hive_id: int, db: SessionLocal = next(get_db())):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail="Hive not found")
    return hive


@app.put("/hives/{hive_id}", response_model=HiveOut)
def update_hive(hive_id: int, updated_data: HiveCreate, db: SessionLocal = next(get_db())):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail="Hive not found")
    for key, value in updated_data.dict().items():
        setattr(hive, key, value)
    db.commit()
    db.refresh(hive)
    return hive


@app.delete("/hives/{hive_id}")
def delete_hive(hive_id: int, db: SessionLocal = next(get_db())):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail="Hive not found")
    db.delete(hive)
    db.commit()
    return {"message": f"Hive {hive_id} deleted successfully"}
