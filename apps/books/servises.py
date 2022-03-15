import sys,os
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("..."))

from fastapi.responses import JSONResponse
from fastapi import status,HTTPException
from sqlalchemy.orm import Session

from apps.books.models import Book, Part
from apps.books import schemas
from apps.users.models  import User


def check(model):
    if model == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='')
    else:
        return model
    
def check_filter(filter):
    if filter.all()==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return filter


def get_books(db: Session):
    return check(db.query(Book).all())


def get_book(db: Session, id: int):
    book = db.query(Book).filter(Book.id == id).first()
    return check(book)


def create_book(db: Session, book:schemas.BookBase):
    db_book = Book(title=book.title,
                       descriptions=book.descriptions,
                       file_path=book.file_path)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def put_book(db: Session, id: int, book: schemas.BookBase):
    book_db = check_filter(db.query(Book).filter(Book.id == id))
    book_db.update(book.dict())
    db.commit()
    return book_db.first()


def patch_book(db: Session, id: int, book: schemas.BookBase):
    book_db = check_filter(db.query(Book).filter(Book.id == id))
    book_db.update(book.dict(exclude_unset=True))
    db.commit()
    return book_db.first()


def delete_book(db: Session, id: int):
    book = check_filter(db.query(Book).filter(Book.id == id))
    db.delete(book)
    db.commit()
    return JSONResponse({"message": f"book with id {id} is deleted"},
                        status_code=status.HTTP_204_NO_CONTENT)
    

# mb i need to set .first()     [65]
def set_books(db:Session,id_books:list[int],id_user:int):
    user = check_filter(db.query(User).filter(User.id == id_user))
    books = db.query(Book).filter(Book.id.in_(id_books)).all()
    user.books = books
    db.commit()
    return user


def get_part(db:Session):
    return check(db.query(Part).all())


def get_parts(db: Session, id: int):
    book = db.query(Part).filter(Part.id == id).first()
    return check(book)


def create_part(db: Session, part:schemas.PartBase,book_id:int):
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

