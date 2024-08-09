from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, index=True)
    operation_type = Column(String(50))
    old_data = Column(JSON)
    new_data = Column(JSON)
    timestamp = Column(DateTime, default=func.now())