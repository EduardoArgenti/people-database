from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.person import Person
from schemas.person import PersonBase, PersonModel, PersonUpdate
import core.database as database
from typing import List, Optional
from services.people import add_person
from services.logs import log_operation, parse_data
from datetime import datetime

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
    query = db.query(Person)

    if filter_column and filter_value:
        if filter_column == 'id':
            filter_value_int = int(filter_value)
            query = query.filter(Person.id == filter_value_int)
        elif filter_column in ['name', 'gender', 'nationality']:
            query = query.filter(getattr(Person, filter_column).ilike(f"%{filter_value}%"))

    if keyword:
        query = query.filter(
            or_(
                Person.name.ilike(f"%{keyword}%"),
                Person.gender.ilike(f"%{keyword}%"),
                Person.nationality.ilike(f"%{keyword}%")
            )
        )

    people = query.offset(skip).limit(limit).all()
    return people

@router.get("/people/{id}", response_model=PersonModel, tags=['People'])
async def fetch_person(id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()
    if person:
        return person
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')

@router.put("/people/{id}", response_model=PersonModel, tags=['People'])
async def update_person(id: int, new_data: PersonUpdate, db: Session = Depends(get_db)):
    person = await fetch_person(id, db)
    if person:
        old_data = parse_data(person)
        update_data = new_data.dict(exclude_unset=True)
        update_data.pop("id", None)
        update_data.pop("created_at", None)

        for key, value in new_data.dict().items():
            setattr(person, key, value)

        person.updated_at = datetime.now()

        db.commit()
        db.refresh(person)
        log_operation(person_id=id, operation_type='update', old_data=old_data, new_data=update_data, db=db)

        return person

@router.delete("/people/{id}", response_model=str, tags=['People'])
async def remove_person(id: int, db: Session = Depends(get_db)):
    person = await fetch_person(id, db)

    if person:
        old_data = parse_data(person)
        db.delete(person)
        db.commit()
        log_operation(person_id=id, operation_type='delete', old_data=old_data, db=db)
        return f'Person ID {id} successfully deleted'