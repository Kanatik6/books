import sys,os
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("..."))

from fastapi.responses import JSONResponse
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from apps.users.auth.jwt_bearer import JWTBearer, get_current_user
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
            response_model=schemas.BookRetrieve
            )
def get_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == id).first()
    return db_book


# create book , enum
@router.post("/",
             response_model=schemas.BookRetrieve,
             dependencies=[Depends(JWTBearer())]
             )
def create_book(*, db: Session = Depends(get_db), book: schemas.BookBase, user_id = Depends(get_current_user)):
    return servises.create_book(book_in=book, db=db, user_id=user_id.get('userID'))


# put book
@router.put("/{id}/",
            response_model=schemas.BookRetrieve,
            dependencies=[Depends(author_permission)]
            )
def put_book(*, db: Session = Depends(get_db),
             book: schemas.BookBase,
             id: int
             ):
    return servises.put_book(book=book, db=db, id=id)


# patch book
@router.patch("/{id}/",
              response_model=schemas.BookRetrieve,
              dependencies=[Depends(author_permission)]
              )
def patch_book(*, db: Session = Depends(get_db),
               book: schemas.BookBase,
               id: int
               ):
    return servises.patch_book(book=book, db=db, id=id)


# delete book
@router.delete("/{id}/",
               dependencies=[Depends(author_permission)])
def delete_book(*, db: Session = Depends(get_db),
                id: int
                ):
    return servises.delete_book(db=db, id=id)




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
@router.get("/{id}/parts/{part_id}/",
            response_model=schemas.PartReturn
            )
def get_part(part_id: int,
             id: int,
             db: Session = Depends(get_db)
             ):
    db_parts = db.query(Part).filter(
        Part.book_id == id, Part.id == part_id)
    return db_parts


# create part , enum
@router.post("/{id}/parts/",
             response_model=schemas.PartReturn,
             dependencies=[Depends(author_permission)]
             )
def create_part(*, db: Session = Depends(get_db),
                part: schemas.PartBase,
                id: int
                ):
    return servises.create_part(db=db, part=part, book_id=id)


# put part
@router.put("/parts/{part_id}/",
            response_model=schemas.PartReturn,
            dependencies=[Depends(author_permission)]
            )
def put_part(*, db: Session = Depends(get_db),
             part: schemas.PartBase,
             id: int):
    return servises.put_part(part=part, db=db, id=id)


# patch part
@router.patch("/parts/{part_id}/",
              response_model=schemas.PartReturn,
              dependencies=[Depends(author_permission)]
              )
def patch_part(*, db: Session = Depends(get_db),
               part: schemas.PartBase,
               id: int):
    return servises.patch_part(part=part, db=db, id=id)


# delete part
@router.delete("/parts/{part_id}/",
               dependencies=[Depends(author_permission)]
               )
def delete_part(*, db: Session = Depends(get_db), part: schemas.PartBase, id: int):
    return servises.delete_part(part=part, db=db, id=id)
