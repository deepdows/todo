from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates, relationship
from datetime import datetime

from database import Base
from todo.models import Todo

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    created_date = Column(DateTime, default=datetime.now)

    todos = relationship('Todo')