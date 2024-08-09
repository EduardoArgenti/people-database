from datetime import date, datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import delete
from pydantic import BaseModel
import models, database, schemas
from io import BytesIO
import pandas as pd

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


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"A simple FastAPI crud using React and PostgreSQL"}

# Person CRUD
@app.post("/people/", response_model=schemas.PersonModel)
async def create_person(person: schemas.PersonBase, db: Session = Depends(get_db)):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/people/", response_model=List[schemas.PersonModel])
async def fetch_people(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    people = db.query(models.Person).offset(skip).limit(limit).all()
    return people

@app.get("/people/{id}", response_model=schemas.PersonModel)
async def fetch_person(id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == id).first()
    if person:
        return person
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')

@app.delete("/people/{id}", response_model=str)
async def remove_person(id: int, db: Session = Depends(get_db)):
    person = await fetch_person(id, db)

    if person:
        db.delete(person)
        db.commit()
        return f'Person ID {id} successfully deleted'
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')

# CSV
@app.post("/people/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)

    # Normalizing dates
    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
    df['data_criacao'] = pd.to_datetime(df['data_criacao'], dayfirst=True, errors='coerce')
    df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao'], dayfirst=True, errors='coerce')

    created_people = []
    for index, row in df.iterrows():
        person_data = {
            "name": row["nome"],
            "birthdate": row["data_nascimento"],
            "gender": row["genero"],
            "nationality": row["nacionalidade"],
            "created_at": row['data_criacao'],
            "updated_at": row['data_atualizacao']
        }

        person_base = schemas.PersonCreateCsv(**person_data)
        created_person = await create_person(person_base, db)
        created_people.append(created_person)

    return {"created_people": f'{len(created_people)} records successfully added to the database.'}

@app.get("/people/download")
async def download_file(db: Session = Depends(get_db)):
    pass