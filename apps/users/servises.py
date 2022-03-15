from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from apps.users.auth.jwt_handler import singJWT
from apps.users.auth.jwt_handler import decodeJWT, get_payload_jwt
from apps.users import schemas
from apps.users.models import User
from apps.books.servises import check_filter
from apps.books.models import Book

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.User):
    # if username is exist, raise exception
    if db.query(User.id).filter_by(username=user.username).first() != None:
        raise HTTPException(
            status_code=400, detail='username must be unique, try again')
    user = User(username=user.username,
                last_name=user.last_name,
                hashed_password=pwd_context.hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(User.id, User.hashed_password).filter(
        User.username == user.username).first()
    print(db_user)
    if not db_user:
        raise HTTPException(status_code=401, detail='user not found')

    if not pwd_context.verify(user.password, db_user[1]):
        raise HTTPException(status_code=401, detail='wrong password')

    tokens = singJWT(db_user[0])
    return tokens


def login_refresh_user(token: str):
    if not decodeJWT(token):
        raise HTTPException(status_code=400, detail='token invalid or expired')
    payload = get_payload_jwt(token)
    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=400, detail='need refresh token')
    token = singJWT(payload.get('id'), type='refresh')
    return token


def delete_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(User).filter_by(
        username=user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail='user not found')
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='wrong password')
    db.delete(db_user)
    db.commit()
    return JSONResponse({'success': True}, status_code=204)


def get_user(db: Session, id: int):
    return db.query(User).filter_by(id=id).first()


def get_users(db: Session):
    return db.query(User).all()


def set_favorites(db: Session, id_books: list[int], id_user: int):
    user = check_filter(db.query(User).filter(User.id == id_user)).first()
    books = db.query(Book).filter(Book.id.in_(id_books)).all()
    user.favorite_books = books
    db.commit()
    return user


def add_favorite(db: Session, id_book: int, id_user: int):
    user = check_filter(db.query(User).filter(User.id == id_user)).first()
    book = db.query(Book).filter(Book.id == id_book).first()
    if book not in user.favorite_books:
        user.favorite_books.append(book)
        db.commit()
    print(user.favorite_books)
    return user


def remove_favorite(db: Session, id_book: int, id_user: int):
    user = check_filter(db.query(User).filter(User.id == id_user)).first()
    user.favorite_books
    book = db.query(Book).filter(Book.id == id_book).first()
    if book in user.favorite_books:
        user.favorite_books.remove(book)
        db.commit()
    return user
