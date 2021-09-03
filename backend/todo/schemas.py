from pydantic import BaseModel
from typing import Optional
from datetime import datetime

def to_camel(string: str) -> str:
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])

class TodoBase(BaseModel):
    title: str
    description: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TodoShow(TodoBase):
    id: int
    is_done: bool
    created_date: datetime

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True