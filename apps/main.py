import sys,os
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("..."))

from fastapi import FastAPI
from apps.database import engine, Base

from apps.users.routers import router as router_user
from apps.books.routers import router as router_book

def create_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Author Today")

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(router=router_user)
app.include_router(router=router_book)
