from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
import core.database as database
from typing import List
from services.csv import upload, download

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/people/upload", tags=['CSV'])
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await upload(file, db)

@router.post("/people/download", tags=['CSV'])
async def download_file(ids: List[int], db: Session = Depends(get_db)):
    return await download(ids, db)