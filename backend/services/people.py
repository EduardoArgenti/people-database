from sqlalchemy.orm import Session
import models, schemas

async def add_person(person: schemas.PersonBase, db: Session):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    # log_operation(db_person.id, 'create', new_data=person.dict(), db=db)
    return db_person