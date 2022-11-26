"""This module contains the functions used to get movie predictions."""

import logging
import heapq

import numpy as np
from surprise import KNNBaseline
import joblib


def get_neighbors(movie_ids: np.ndarray,
                  model: KNNBaseline = None,
                  k: int = 4) -> np.ndarray:
    """
    Predicts movie recommendtions on array of movies ids.

    Parameters
    ----------
    movie_ids : numpy.ndarray
        1D numpy array containing movie ids.
    model : surprise.KNNBaseline, optional
        KNNBaseline model. The model containing the similarity matrix.
        If not passed, the default model will be used.
    k : int, optional
        The number of neighbors to be returned.

    Returns
    -------
    numpy.ndarray
        Numpy array with the movie ids and similarity scores
        for the k neighbors.
    """
    if model is None:
        try:
            model = load_default_model()
        except Exception as exc:
            logging.error("Failed to load default model.")
            raise Exception("Missing default model.") from exc
    return [make_prediction(movie_id, model, k) for movie_id in movie_ids]


def load_default_model() -> KNNBaseline:
    """
    Load from disk and return default KNNBaseline model using joblib

    Returns
    -------
    surprise.KNNBaseline
        The loaded default model.
    """
    model = joblib.load('models/model.joblib')
    return model


def make_prediction(movie_id: int, model: KNNBaseline, k: int) -> np.ndarray:
    """
    Predicts movie recommendtions on movie id.

    Parameters
    ----------
    movie_id : int
        The movie id.
    model : surprise.KNNBaseline
        KNNBaseline model. The model containing the similarity matrix.
    k : int
        The number of neighbors to be returned.

    Returns
    -------
    numpy.ndarray
        Numpy array with the movie id and similarity scores
        for the k neighbors.
    """
    inner_id = get_inner_movie_id(model, movie_id)
    k_neighbors = get_k_nearest_neighors(model, inner_id, k)
    return k_neighbors


def get_inner_movie_id(model: KNNBaseline, movie_id: int) -> int:
    """
    Transform movie id into its inner representation.

    Parameters
    ----------
    model : surprise.KNNBaseline
        KNNBaseline model.
    movie_id : int
        The movie id.

    Returns
    -------
    int
        The inner movie id.
    """
    return model.trainset.to_inner_iid(movie_id)


def get_k_nearest_neighors(model: KNNBaseline,
                           inner_id: int,
                           k: int) -> np.ndarray:
    """
    Get K movie neighbors with their similarity scores.

    Parameters
    ----------
    model : surprise.KNNBaseline
        KNNBaseline model.
    inner_id : int
        The movie inner id.
    k : int
        The number of neighbors to return

    Returns
    -------
    numpy.ndarray
        An array containing tuples of K nearest movie inner ids,
        and their similarity scores.
    """
    neighbors = get_all_neighbors(model, inner_id)
    k_neighbors = heapq.nlargest(k, neighbors, key=lambda tple: tple[1])
    return k_neighbors


def get_all_neighbors(model: KNNBaseline, inner_id: int) -> np.ndarray:
    """
    Get all movie neighbors with their similarity scores.

    Parameters
    ----------
    model : surprise.KNNBaseline
        KNNBaseline model.
    inner_id : int
        The movie inner id.

    Returns
    -------
    numpy.ndarray
        An array containing tuples of all other movie inner ids,
        and their similarity scores.
    """
    movie_row = model.sim[inner_id, :].copy()
    movie_row[movie_row == 1] = movie_row.min()
    max_score = movie_row.max()
    return [(model.trainset.to_raw_iid(index), score / max_score)
            for index, score in enumerate(movie_row)]
