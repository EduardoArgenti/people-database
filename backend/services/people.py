from sqlalchemy.orm import Session
from models.person import Person
from schemas.person import PersonBase, PersonModel, PersonUpdate
from services.logs import log_operation, parse_data
from typing import Optional
import core.database as database
from fastapi import Depends, HTTPException
from sqlalchemy import or_
from datetime import datetime


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def add_person(person: PersonBase, db: Session):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    log_operation(db_person.id, 'create', new_data=person.dict(), db=db)
    return db_person


async def get_people(
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

    return [PersonModel.from_orm(person) for person in people]


async def get_person(id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()
    if person:
        return person
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')


async def put_person(id:int, new_data: PersonUpdate, db: Session = Depends(get_db)):
    person = await get_person(id, db)
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


async def delete_person(id:int, db: Session = Depends(get_db)):
    person = await get_person(id, db)

    if person:
        old_data = parse_data(person)
        db.delete(person)
        db.commit()
        log_operation(person_id=id, operation_type='delete', old_data=old_data, db=db)
        return f'Person ID {id} successfully deleted'