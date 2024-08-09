from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.person import Person
from schemas.person import PersonBase, PersonModel, PersonUpdate
import core.database as database
from typing import List, Optional
from services.people import add_person, get_people, get_person, put_person, delete_person
from services.logs import log_operation, parse_data

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/people/", response_model=PersonModel, tags=['People'])
async def create_person(person: PersonBase, db: Session = Depends(get_db)):
    return await add_person(person, db)

@router.get("/people/", response_model=List[PersonModel], tags=['People'])
async def fetch_people(
    skip: int = 0,
    limit: int = 100,
    filter_column: Optional[str] = None,
    filter_value: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return await get_people(skip, limit, filter_column, filter_value, keyword, db)

@router.get("/people/{id}", response_model=PersonModel, tags=['People'])
async def fetch_person(id: int, db: Session = Depends(get_db)):
    return await get_person(id, db)

@router.put("/people/{id}", response_model=PersonModel, tags=['People'])
async def update_person(id: int, new_data: PersonUpdate, db: Session = Depends(get_db)):
    return await put_person(id, new_data, db)

@router.delete("/people/{id}", response_model=str, tags=['People'])
async def remove_person(id: int, db: Session = Depends(get_db)):
    return await delete_person(id, db)