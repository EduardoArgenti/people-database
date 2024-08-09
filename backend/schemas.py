from pydantic import BaseModel
from datetime import date, datetime

class PersonBase(BaseModel):
    name: str
    birthdate: date
    gender: str
    nationality: str

class PersonCreateCsv(PersonBase):
    created_at: datetime
    updated_at: datetime

class PersonModel(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True