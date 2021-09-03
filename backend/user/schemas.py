from pydantic import BaseModel


class AuthSchema(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    username: str

    class Config:
        orm_mode = True