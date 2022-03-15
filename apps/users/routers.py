from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Body

from apps.database import get_db
from apps.users import schemas, servises
from apps.users.auth.jwt_bearer import get_current_user
from apps.users.models import User
from apps.users.auth.jwt_bearer import JWTBearer


router = APIRouter(prefix='/users')


@router.post('/sing-up/', response_model=schemas.UserRetrieve, tags=['user'])
async def create_user(*, db: Session = Depends(get_db), user: schemas.User):
    user = servises.create_user(db=db, user=user)
    return user


@router.post('/sing-in/', tags=['user'])
async def login_user(*, db: Session = Depends(get_db), user: schemas.UserLogin, tags=['user']):
    return servises.login_user(db=db, user=user)


@router.post('/sing-in/refresh_token', tags=['user'])
async def refresh_user(token:str=Body(...,)):
    return servises.login_refresh_user(token=token)


@router.get('/retrieve', response_model=schemas.UserRetrieve,tags=['user'])
async def get_user(*, db: Session = Depends(get_db),id:int):
    return servises.get_user(db=db,id=id)


@router.get('/all', response_model=list[schemas.UserRetrieve], tags=['user'])
async def get_user(*, db: Session = Depends(get_db)):
    return servises.get_users(db=db)


@router.get('/me', response_model=schemas.UserRetrieve, tags=['user'])
async def get_user(*, db: Session = Depends(get_db),user_id:int = Depends(get_current_user)):
    return db.query(User).filter_by(id=user_id.get('userID')).first()


# set books
@router.post("/set_favorites/",
             response_model=schemas.UserRetrieve,
             dependencies=[Depends(JWTBearer())], 
             tags=['user']
             )
def set_favorite(*, db: Session = Depends(get_db),
             book_ids: list[int],
             user_id = Depends(get_current_user)
             ):
    return servises.set_favorites(id_books=book_ids, id_user=user_id.get('userID'), db=db)


@router.post("/add_favorite/",
             response_model=schemas.UserRetrieve,
             dependencies=[Depends(JWTBearer())],
             tags=['user'])
def add_favorite(*, db: Session = Depends(get_db),
             book_ids: int,
             user_id = Depends(get_current_user)
             ):
    return servises.add_favorite(id_book=book_ids, id_user=user_id.get('userID'), db=db)



@router.post("/remove_favorite/",
             response_model=schemas.UserRetrieve,
             dependencies=[Depends(JWTBearer())],
             tags=['user'])
def remove_favorite(*, db: Session = Depends(get_db),
             book_ids: int,
             user_id = Depends(get_current_user)
             ):
    return servises.remove_favorite(id_book=book_ids, id_user=user_id.get('userID'), db=db)