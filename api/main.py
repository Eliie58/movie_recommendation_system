"""
Module for FastAPI endpoints
"""
import random
from typing import List
import logging

from fastapi import FastAPI

from .database import Database, Prediction, Movie, Genre

app = FastAPI()
db = Database.instance()
logging.basicConfig(level=logging.INFO)


@app.get("/genres")
def get_genres() -> List[Genre]:
    """
    Get all movie genres endpoint.
    """
    return db.fetch_genres()


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
    return db.fetch_movies_by_genre_and_title(genre_id, title)


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
    return db.fetch_predictions(prediction_id, number_of_movies)


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
    movies = db.fetch_movies()
    predictions = random.sample(movies, 4)
    return db.store_prediction(movie_id, predictions)
