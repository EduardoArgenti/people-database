from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/logs/", response_model=List[schemas.LogModel], tags=['Logs'])
async def fetch_logs(db: Session = Depends(get_db)):
    logs = db.query(models.Log).all()
    return logs