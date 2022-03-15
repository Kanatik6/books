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
    favorite_books: "list[Book]"

    class Config:
        orm_mode = True


class UserRetrieve(BaseModel):
    id: int
    username: str
    last_name: str
    favorite_books: "list[Book]"
    author_books: "list[Book]"

    class Config:
        orm_mode = True


class UserWOBook(BaseModel):
    id: int
    username: str
    last_name: str

    class Config:
        orm_mode = True


from apps.books.schemas import BookReturn, Book
UserRetrieve.update_forward_refs()
ReturnUser.update_forward_refs()