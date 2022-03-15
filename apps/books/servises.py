import sys,os
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("..."))

from fastapi.responses import JSONResponse
from fastapi import status,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from apps.users.models  import User
from apps.books.models import Book, Part
from apps.books import schemas


def check(model):
    if model == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='not found')
    else:
        return model


def check_filter(filter):
    if filter.all() == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return filter


def get_books(db: Session):
    return check(db.query(Book).all())


def get_book(db: Session, id: int):
    book = db.query(Book).filter(Book.id == id).first()
    return check(book)


def create_book(db: Session, book_in: schemas.BookBase, user_id: int):
    if db.query(Book).filter_by(title=book_in.title).first():
        return JSONResponse({'message': 'title and file_name must be unique,try again'}, status_code=400)
    author_books_file = db.query(Book.file_name).filter(
        Book.author.has(User.id == user_id)).first()

    if author_books_file != None:
        if book_in.file_name in author_books_file:
            return JSONResponse({'message': 'title and file_name must be unique,try again'}, status_code=400)

    user = db.query(User).filter_by(id=user_id).first()
    book = Book(title=book_in.title,
                descriptions=book_in.descriptions,
                file_name=book_in.file_name,
                author=user)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def put_book(db: Session, id: int, book: schemas.BookBase):
    book_db = check_filter(db.query(Book).filter(Book.id == id))
    if db.query(Book.id).filter(or_(Book.title == book.title, Book.file_name == book.file_name)).first():
        return JSONResponse({'message': 'title and file_name must be unique,try again'}, status_code=400)
    book_db.update(book.dict())
    db.commit()
    return book_db.first()


def patch_book(db: Session, id: int, book: schemas.BookBase):
    book_db = check_filter(db.query(Book).filter(Book.id == id))
    if db.query(Book.id).filter(or_(Book.title == book.title, Book.file_name == book.file_name)).first():
        return JSONResponse({'message': 'title and file_name must be unique,try again'}, status_code=400)
    book_db.update(book.dict(exclude_unset=True))
    db.commit()
    return book_db.first()


def delete_book(db: Session, id: int):
    book = check(db.query(Book).filter(Book.id == id).first())
    db.delete(book)
    db.commit()
    return JSONResponse({"message": f"book with id {id} is deleted"},
                        status_code=status.HTTP_204_NO_CONTENT)



def get_part(db: Session):
    return check(db.query(Part).all())


def get_parts(db: Session, id: int):
    book = db.query(Part).filter(Part.id == id).first()
    return check(book)


def create_part(db: Session, part: schemas.PartBase, book_id: int):
    part = Part(title=part.title,
                descriptions=part.descriptions,
                book_id=book_id)
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


def put_part(db: Session, id: int, part: schemas.BookBase):
    part_db = check_filter(db.query(Part).filter(Part.id == id))
    part_db.update(part.dict())
    db.commit()
    return part_db.first()


def patch_part(db: Session, id: int, part: schemas.BookBase):
    part_db = check_filter(db.query(Part).filter(Part.id == id))
    part_db.update(part.dict(exclude_unset=True))
    db.commit()
    return part_db.first()


def delete_part(db: Session, id: int):
    part = check_filter(db.query(Part).filter(Part.id == id))
    db.delete(part)
    db.commit()
    return JSONResponse({"message": f"part with id {id} is deleted"},
                        status_code=status.HTTP_204_NO_CONTENT)
