from pydantic import BaseModel
from fastapi import Form
from sqlalchemy.sql.operators import as_


def as_form(cls : type[BaseModel]) -> type[BaseModel]:
    cls.__signature__ = cls.__signature__.replace(
        parameters = [
            param.replace(default = Form(...))
            for param in cls.__signature__.parameters.values()
        ]
    )
    return cls

@as_form
class UserBase(BaseModel):
    name: str

@as_form
class UserCreate(UserBase):
    password: str

@as_form
class User(UserCreate):
    id: int
    class Config:
        orm_mode = True

class Post():
    pass
