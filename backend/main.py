from datetime import datetime, date
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, database, schemas
import pandas as pd
import io

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


def serialize_dates(data):
    if isinstance(data, dict):
        return {k: serialize_dates(v) for k, v in data.items()}
    if isinstance(data, list):
        return [serialize_dates(i) for i in data]
    if isinstance(data, (datetime, date)):
        return data.isoformat()
    return data


def log_operation(person_id: int, operation_type: str, old_data=None, new_data=None, db: Session = Depends(get_db)):
    log_entry = models.Log(
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
    log_operation(db_person.id, 'create', new_data=person.dict(), db=db)
    return db_person

@app.get("/people/", response_model=List[schemas.PersonModel])
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

@app.get("/people/{id}", response_model=schemas.PersonModel)
async def fetch_person(id: int, db: Session = Depends(get_db)):
    person = db.query(models.Person).filter(models.Person.id == id).first()
    if person:
        return person
    raise HTTPException(status_code=404, detail=f'Person ID {id} not found')

@app.put("/people/{id}", response_model=schemas.PersonModel)
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

@app.delete("/people/{id}", response_model=str)
async def remove_person(id: int, db: Session = Depends(get_db)):
    person = await fetch_person(id, db)

    if person:
        old_data = parse_data(person)
        db.delete(person)
        db.commit()
        log_operation(person_id=id, operation_type='delete', old_data=old_data, db=db)
        return f'Person ID {id} successfully deleted'

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

@app.post("/people/download")
async def download_file(ids: List[int], db: Session = Depends(get_db)):
    people = db.query(models.Person).filter(models.Person.id.in_(ids)).all()

    if people:
        df = pd.DataFrame([person.__dict__ for person in people])
        if '_sa_instance_state' in df.columns:
            df.drop(columns=['_sa_instance_state'], inplace=True)

        df.drop(columns=['id'], inplace=True)

        df.rename(columns={
            'name': 'nome',
            'birthdate': 'data_nascimento',
            'gender': 'genero',
            'nationality': 'nacionalidade',
            'created_at': 'data_criacao',
            'updated_at': 'data_atualizacao'
        }, inplace=True)

        column_order = ['nome', 'data_nascimento', 'genero', 'nacionalidade', 'data_criacao', 'data_atualizacao']

        df = df[column_order]

        csv = df.to_csv(index=False)

        return StreamingResponse(io.StringIO(csv), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=filtered_people.csv"})
    raise HTTPException(status_code=404, detail="No records found")