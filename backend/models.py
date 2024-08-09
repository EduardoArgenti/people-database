from database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, JSON
from sqlalchemy.sql import func


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, index=True)
    operation_type = Column(String(50))
    old_data = Column(JSON)
    new_data = Column(JSON)
    timestamp = Column(DateTime, default=func.now())


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birthdate = Column(Date)
    gender = Column(String(20))
    nationality = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())