from sqlalchemy.orm import Session
from models.person import Person
from schemas.person import PersonBase
from services.logs import log_operation

async def add_person(person: PersonBase, db: Session):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    log_operation(db_person.id, 'create', new_data=person.dict(), db=db)
    return db_person