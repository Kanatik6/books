from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from decouple import config

USER = config('user')
PASSWORD = config('password')
DB = config('db')
HOST = config('host')


SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print('base')
Base = declarative_base()

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
