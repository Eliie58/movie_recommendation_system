from typing import Union

from fastapi import FastAPI
from .database import Database

app = FastAPI()


@app.get("/")
def read_root():
    db: Database = Database.instance()
    db.fetchAllUsers()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
