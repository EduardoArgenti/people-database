from pydantic import BaseModel
from datetime import date, datetime


class LogModel(BaseModel):
    id: int
    person_id: int
    operation_type: str
    timestamp: datetime
    old_data: dict = None
    new_data: dict = None

    class Config:
        orm_mode = True