from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from models.log import Log
from schemas.log import LogModel
import core.database as database

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/logs/", response_model=List[LogModel], tags=['Logs'])
async def fetch_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return logs