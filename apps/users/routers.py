from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Body

from apps.database import get_db
from apps.users import schemas, servises

router = APIRouter(prefix='/users')


@router.post('/sing-up/', response_model=schemas.ReturnUser, tags=['user'])
async def create_user(*, db: Session = Depends(get_db), user: schemas.User):
    user = servises.create_user(db=db, user=user)
    return user


@router.post('/sing-in/', tags=['user'])
async def login_user(*, db: Session = Depends(get_db), user: schemas.UserLogin, tags=['user']):
    return servises.login_user(db=db, user=user)


@router.post('/sing-in/refresh_token', tags=['user'])
async def refresh_user(token:str=Body(...,)):
    return servises.login_refresh_user(token=token)
