from sqlalchemy.orm import Session
from fastapi import Depends
from models.log import Log
import core.database as database
from datetime import date, datetime


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def log_operation(person_id: int, operation_type: str, old_data=None, new_data=None, db: Session = Depends(get_db)):
    log_entry = Log(
        person_id=person_id,
        operation_type=operation_type,
        old_data=serialize_dates(old_data),
        new_data=serialize_dates(new_data)
    )
    db.add(log_entry)
    db.commit()


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


def serialize_dates(data):
    if isinstance(data, dict):
        return {k: serialize_dates(v) for k, v in data.items()}
    if isinstance(data, list):
        return [serialize_dates(i) for i in data]
    if isinstance(data, (datetime, date)):
        return data.isoformat()
    return data