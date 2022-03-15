from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    descriptions: str
    file_path:str

    class Config:
        orm_mode = True


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


class BookReturn(BaseModel):
    id: int
    title: str
    descriptions: str
    file_path: str
    parts: list[PartReturn] | None = None

    class Config:
        orm_mode = True
