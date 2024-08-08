from datetime import date, datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
import models, database

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class PersonBase(BaseModel):
    name: str
    birthdate: date
    gender: str
    nationality: str

class PersonModel(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"A simple FastAPI crud using React and Postgres"}

@app.post("/people/", response_model=PersonModel)
async def create_person(person: PersonBase, db: Session = Depends(get_db)):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/people/", response_model=List[PersonModel])
async def fetch_people(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    people = db.query(models.Person).offset(skip).limit(limit).all()
    return people

@app.get("/people/{id}", response_model=PersonModel)
async def fetch_person(id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == id).first()
    if person:
        return person
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')