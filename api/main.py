"""
Module for FastAPI endpoints
"""

from typing import List
import logging

from fastapi import FastAPI
from pydantic import BaseModel

from .database import Database, Prediction, Movie, Genre
from .inference import get_neighbors, load_model


app = FastAPI()
DB = Database.instance()
model = load_model('/models/model.joblib')
logging.basicConfig(level=logging.INFO)


@app.get("/genres")
def get_genres() -> List[Genre]:
    """
    Get all movie genres endpoint.
    """
    return DB.fetch_genres()


@app.get("/movies")
def get_movies_by_genre_and_title(genre_id: int, title: str) -> List[Movie]:
    """
    Get all movies filtered by genre and title.

    Parameters
    ----------
    genre_id : int
        Movie genre id, used to filter the returned movies.
    title : str
        Movie title, used to filter the returned movies.

    Returns
    -------
    list
        List of movies
    """
    logging.info('Getting movies for genre %s and title like %s',
                 genre_id, title)
    return DB.fetch_movies_by_genre_and_title(genre_id, title)


@app.get("/history")
def get_history(prediction_id: int = 0,
                number_of_movies: int = 10) -> List[Prediction]:
    """
    Get previous predictions endpoint.

    Parameters
    ----------
    prediction_id : int, optional
        Prediction id, optional parameter, used to get details for
        a specific prediction.
    number_of_movies : int, optional
        Used to specify the number of previous predictions to return,
        default value is 10.

    Returns
    -------
    list
        List of predictions
    """
    return DB.fetch_predictions(prediction_id, number_of_movies)


@app.get("/single-prediction")
def single_prediction(movie_id: int) -> int:
    """
    Get a prediction for a single movie.

    Parameters
    ----------
    movie_id : int
        Movie id, used to find similar movies.

    Returns
    -------
    int
        Prediction Id
    """
    predictions = get_neighbors([movie_id], model=model, k=4)[0]
    return DB.store_prediction(movie_id, predictions)


class MovieIdList(BaseModel):
    """Movie Id Pydantic Model"""
    ids: List[int]


@app.post("/upload/")
def upload(movies_id: MovieIdList) -> List[int]:
    """
    Get predictions for a multiple movies.

    Parameters
    ----------
    movies_id : MovieIdList
        Movie ids, used to find similar movies.

    Returns
    -------
    List
        Prediction Ids
    """
    prediction_ids = [single_prediction(movie_id)
                      for movie_id in movies_id.ids]
    return prediction_ids
