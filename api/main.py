from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from .database import Database, Prediction
import random

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/genres")
def read_genres():
    db: Database = Database.instance()
    return db.fetch_genres()


@app.get("/movies")
def movies_by_genre(genre_id: int, title: str):
    print(f'Getting movies for genre {genre_id} and title like {title}')
    db: Database = Database.instance()
    return db.fetch_movies_by_genre(genre_id, title)


@app.get("/history")
def prediction_history(id: int = 0):
    db: Database = Database.instance()
    return db.fetch_predictions(id, n=10)


@app.get("/single-prediction")
def single_prediction(movie_id: int):
    db: Database = Database.instance()
    movies = db.fetch_movies()
    predictions = random.sample(movies, 4)
    return db.store_prediction(movie_id, predictions)


class MovieIdList(BaseModel):
    ids: List[int]


@app.post("/upload/")
def upload(movies_id: MovieIdList):
    db: Database = Database.instance()
    movie_list = [single_prediction(movie_id) for movie_id in movies_id.ids]
    return movie_list
