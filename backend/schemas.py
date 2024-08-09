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

class PersonUpdate(PersonBase):
    pass

class PersonModel(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LogModel(BaseModel):
    id: int
    person_id: int
    operation_type: str
    timestamp: datetime
    old_data: dict = None
    new_data: dict = None

    class Config:
        orm_mode = True