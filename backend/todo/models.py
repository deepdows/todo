from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import validates
from datetime import datetime

from database import Base

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)