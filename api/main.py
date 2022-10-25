from fastapi import FastAPI
from .database import Database
import random

app: FastAPI = FastAPI()
db: Database = Database.instance()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/genres")
def read_genres():
    return db.fetch_genres()


@app.get("/movies")
def movies_by_genre(genre_id: int, title: str):
    print(f'Getting movies for genre {genre_id} and title like {title}')
    return db.fetch_movies_by_genre(genre_id, title)


@app.get("/history")
def prediction_history(id: int = 0):
    return db.fetch_predictions(id, n=10)


@app.get("/single-prediction")
def single_prediction(movie_id: int):
    movies = db.fetch_movies()
    predictions = random.sample(movies, 4)
    return db.store_prediction(movie_id, predictions)
