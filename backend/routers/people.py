from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from typing import List, Optional
from services.people import add_person
from datetime import datetime, date

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/people/", response_model=schemas.PersonModel, tags=['People'])
async def create_person(person: schemas.PersonBase, db: Session = Depends(get_db)):
    return await add_person(person, db)

@router.get("/people/", response_model=List[schemas.PersonModel], tags=['People'])
async def fetch_people(
    skip: int = 0,
    limit: int = 100,
    filter_column: Optional[str] = None,
    filter_value: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Person)

    if filter_column and filter_value:
        if filter_column == 'id':
            filter_value_int = int(filter_value)
            query = query.filter(models.Person.id == filter_value_int)
        elif filter_column in ['name', 'gender', 'nationality']:
            query = query.filter(getattr(models.Person, filter_column).ilike(f"%{filter_value}%"))

    if keyword:
        query = query.filter(
            or_(
                models.Person.name.ilike(f"%{keyword}%"),
                models.Person.gender.ilike(f"%{keyword}%"),
                models.Person.nationality.ilike(f"%{keyword}%")
            )
        )

    people = query.offset(skip).limit(limit).all()
    return people

@router.get("/people/{id}", response_model=schemas.PersonModel, tags=['People'])
async def fetch_person(id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == id).first()
    if person:
        return person
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')

@router.put("/people/{id}", response_model=schemas.PersonModel, tags=['People'])
async def update_person(id: int, new_data: schemas.PersonUpdate, db: Session = Depends(get_db)):
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


def parse_data(person):
    parsed_data = {
        "id": person.id,
        "name": person.name,
        "birthdate": person.birthdate,
        "gender": person.gender,
        "nationality": person.nationality,
        "created_at": person.created_at,
        "updated_at": person.updated_at
    }

    return parsed_data


def log_operation(person_id: int, operation_type: str, old_data=None, new_data=None, db: Session = Depends(get_db)):
    log_entry = models.Log(
        person_id=person_id,
        operation_type=operation_type,
        old_data=serialize_dates(old_data),
        new_data=serialize_dates(new_data)
    )
    db.add(log_entry)
    db.commit()


def serialize_dates(data):
    if isinstance(data, dict):
        return {k: serialize_dates(v) for k, v in data.items()}
    if isinstance(data, list):
        return [serialize_dates(i) for i in data]
    if isinstance(data, (datetime, date)):
        return data.isoformat()
    return data