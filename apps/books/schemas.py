from pydantic import BaseModel, Field


class PartBase(BaseModel):
    title:str
    descriptions: str

    class Config:
        orm_mode = True


class PartReturn(BaseModel):
    id:int
    title:str
    descriptions: str

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str = Field(...)
    descriptions: str
    file_name:str

    class Config:
        orm_mode = True


class Book(BaseModel):
    id:int
    title: str = Field(...)
    descriptions: str
    file_name:str
    parts: list[PartReturn] |None = None

    class Config:
        orm_mode = True


class BookReturn(BaseModel):
    id: int
    author : "UserWOBook"
    title: str
    descriptions: str
    file_name: str
    parts: list[PartReturn] |None = None

    class Config:
        orm_mode = True


class BookRetrieve(BaseModel):
    id: int
    title: str
    descriptions: str
    file_name: str
    parts: list[PartReturn] |None = None
    author : "UserWOBook"
    parts: list[PartReturn] |None = None

    class Config:
        orm_mode = True

from apps.users.schemas import UserWOBook
BookRetrieve.update_forward_refs()
BookReturn.update_forward_refs()