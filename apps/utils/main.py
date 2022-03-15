import sys,os
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("..."))

from fastapi import FastAPI
from database import engine, Base

# from products.routers import router as router_product
from users.routers import router as router_user
from books.routers import router as router_book


def create_db():
    print('Запускается')
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Author today",debug=True)

@app.on_event("startup")
def on_startup():
    create_db()

# app.include_router(router=router_product)
app.include_router(router=router_user)
app.include_router(router=router_book)
