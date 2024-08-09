from fastapi import APIRouter, Depends, HTTPException, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import models, schemas, database
from typing import List, Optional
from datetime import datetime, date
import pandas as pd
from services.people import add_person

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/people/upload", tags=['CSV'])
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
        created_person = await add_person(person_base, db)
        created_people.append(created_person)

    return {"created_people": f'{len(created_people)} records successfully added to the database.'}

@router.post("/people/download", tags=['CSV'])
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