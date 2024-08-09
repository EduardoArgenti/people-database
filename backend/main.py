from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, database, schemas
import io
from routers import people, csv, logs

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

@app.get("/")
def read_root():
    return {"A simple FastAPI crud using React and PostgreSQL"}

# Person CRUD
app.include_router(people.router)

# CSV
app.include_router(csv.router)

# Logs
app.include_router(logs.router)