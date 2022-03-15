import sys,os
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("..."))

from fastapi.responses import JSONResponse
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from apps.users.auth.jwt_bearer import JWTBearer
from apps.utils.permissions import author_permission
from apps.database import get_db
from apps.books.models import Book, Part
from apps.books import schemas, servises


router = APIRouter(prefix='/books')


# get list book
@router.get("/",
            response_model=list[schemas.BookReturn]
            )
def get_books(db: Session = Depends(get_db)):
    db_book = db.query(Book).all()
    if db_book:
        return db_book
    return JSONResponse({'message': 'no books'})


# get retrieve book
@router.get("/{id}/",
            response_model=schemas.BookReturn
            )
def get_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    return db_book


# create book , enum
@router.post("/",
             response_model=schemas.BookReturn,
             dependencies=[Depends(JWTBearer())]
             )
def create_book(*, db: Session = Depends(get_db), book: schemas.BookBase):
    return servises.create_book(book=book, db=db)


# put book
@router.put("/{id}/",
            response_model=schemas.BookReturn,
            dependencies=[Depends(author_permission)]
            )
def put_book(*, db: Session = Depends(get_db),
                   book: schemas.BookBase,
                   id: int
                   ):
    return servises.put_book(book=book, db=db, id=id)


# patch book
@router.patch("/{id}/",
              response_model=schemas.BookReturn,
              dependencies=[Depends(JWTBearer())]
              )
def patch_book(*, db: Session = Depends(get_db),
                     book: schemas.BookBase,
                     id: int
                     ):
    return servises.patch_book(book=book, db=db, id=id)


# delete book
@router.delete("/{id}/",
            dependencies=[Depends(JWTBearer())])
def delete_book(*, db: Session = Depends(get_db),
                      book: schemas.BookBase,
                      id: int
                      ):
    return servises.delete_book(book=book, db=db, id=id)


# set books
@router.post("/",
            dependencies=[Depends(JWTBearer())])
def set_book(*, db: Session = Depends(get_db),
                   book_ids: list[int],
                   user_id: int
                   ):
    return servises.set_books(id_books=book_ids, id_user=user_id, db=db)


# ------------------------------------------------------------------------


# get list part
@router.get("/{book_id}/parts/",
            response_model=list[schemas.PartReturn]
            )
def get_parts(*, db: Session = Depends(get_db),
                    book_id: int
                    ):
    db_parts = db.query(Part).filter(Part.book_id == book_id).all()
    if db_parts:
        return db_parts
    return JSONResponse({'message': 'no parts'})


# get retrieve part
@router.get("/{book_id}/parts/{part_id}/",
            response_model=schemas.PartReturn
            )
def get_part(part_id: int,
                   book_id: int,
                   db: Session = Depends(get_db)
                   ):
    db_parts = db.query(Part).filter(
        Part.book_id == book_id, Part.id == part_id)
    return db_parts


# create part , enum
@router.post("/{book_id}/parts/",
             response_model=schemas.PartReturn,
            dependencies=[Depends(JWTBearer())]
             )
def create_part(*, db: Session = Depends(get_db),
                      part: schemas.PartBase,
                      book_id: int
                      ):
    return servises.create_part(db=db, part=part, book_id=book_id)


# put part
@router.put("/parts/{part_id}/",
            response_model=schemas.PartReturn,
            dependencies=[Depends(JWTBearer())]
            )
def put_part(*, db: Session = Depends(get_db),
                   part: schemas.PartBase,
                   id: int):
    return servises.put_part(part=part, db=db, id=id)


# patch part
@router.patch("/parts/{part_id}/",
              response_model=schemas.PartReturn,
            dependencies=[Depends(JWTBearer())]
              )
def patch_part(*, db: Session = Depends(get_db),
                     part: schemas.PartBase,
                     id: int):
    return servises.patch_part(part=part, db=db, id=id)


# delete part
@router.delete("/parts/{part_id}/",
            dependencies=[Depends(JWTBearer())])
def delete_part(*, db: Session = Depends(get_db), part: schemas.PartBase, id: int):
    return servises.delete_part(part=part, db=db, id=id)


# permissions is user author

# i need to create file
# i need create validation for empty requests
