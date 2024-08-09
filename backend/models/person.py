from core.database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birthdate = Column(Date)
    gender = Column(String(20))
    nationality = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())