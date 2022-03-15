from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import Depends
from decouple import config

from users.auth.jwt_bearer import JWTBearer
from apps.books.models import Book
from users.models import User
from database import get_db
import jwt

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def test_permission(*,token: str = Depends(JWTBearer()),db:Session = Depends(get_db),id:int):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM], verify_signature=False)
    user_books = db.query(User.books).filter_by(id=payload.get("userID")).first()
    book = db.query(Book).filter_by(id=id).first()
    print(user_books)
    if book not in user_books:
        raise HTTPException(status_code=403,detail='not permitted')
