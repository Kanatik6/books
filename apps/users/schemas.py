from pydantic import BaseModel, Field


class User(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    last_name: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=5, max_length=100)

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=5, max_length=100)

    class Config:
        orm_mode = True


class ReturnUser(BaseModel):
    id: int
    username: str
    last_name: str

    class Config:
        orm_mode = True
