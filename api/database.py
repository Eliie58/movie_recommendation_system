"""
Module for SqlAlchemy related classes
"""

import os
import logging

import sqlalchemy as db
from sqlalchemy import Table, Column, String, Integer, \
    ForeignKey, DateTime, Float
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from .Utils import read_movies

logging.basicConfig(level=logging.INFO)


class Database():
    """
    Database functionality wrapper. Use this class
    for all interactions with the database.
    Always use the instance method.

    Example usage:
    db = Database.instance()
    """
    engine = db.create_engine(os.environ["DATABASE_URL"])
    db_instance = None

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")
        try:
            seed(Session(bind=self.connection))
        except Exception as exc:
            logging.exception(exc)

    def fetch_movies_by_genre_and_title(self, genre_id, title):
        """
        Fetch movies filterd by genre id and title.

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
        session = Session(bind=self.connection)
        return session.query(Movie)\
            .filter(Movie.title.ilike(f"%{title}%"))\
            .filter(Movie.genres.any(id=genre_id))\
            .order_by(Movie.year.desc()).all()

    def fetch_genres(self):
        """
        Fetch movie genres.

        Returns
        -------
        list
            List of genres
        """
        session = Session(bind=self.connection)
        return session.query(Genre).all()

    def fetch_predictions(self, prediction_id, number_of_movies):
        """
        Fetch predictions.

        Parameters
        ----------
        prediction_id : int
            Prediction Id. If 0, return "number_of_movies"
            previous predictions.
        number_of_movies : int
            Number of predictions to be returned.

        Returns
        -------
        list
            List of Predictions.
        """
        session = Session(bind=self.connection)
        if prediction_id == 0:
            return session.query(Prediction)\
                .order_by(Prediction.time_stamp.desc())\
                .limit(number_of_movies).all()
        else:
            return session.query(Prediction)\
                .filter(Prediction.id == prediction_id).all()

    def store_prediction(self, movie_id, predictions):
        """
        Store predictions.

        Parameters
        ----------
        movie_id : int
            The id of the movie used for prediction.
        predictions : list
            List of the ids and similarity score of the movies that are
            predicted as similar.

        Returns
        -------
        int
            Prediction Id stored in the database.
        """
        session = Session(bind=self.engine.connect())
        prediction = Prediction(movie_id=movie_id)
        session.add(prediction)
        session.commit()
        for (movie_id, score) in predictions:
            pred_value = PredictionValue(
                movie_id=movie_id, score=score, prediction_id=prediction.id)
            session.add(pred_value)
        session.commit()
        return prediction.id

    @staticmethod
    def instance():
        """
        Static method to get an instance of the Database.

        Returns
        -------
        Database
            Instance of the Database
        """
        if Database.db_instance is None:
            Database.db_instance = Database()
        return Database.db_instance


Base = declarative_base()

movie_genre_table = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movie.id")),
    Column("genre_id", ForeignKey("genre.id"))
)


class Movie(Base):
    """SQL Alchemy Model for Movie."""
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    genres = relationship("Genre", secondary=movie_genre_table, lazy="joined")

    def __repr__(self):
        return f"<Movie(id='{self.id}', title='{self.title}',\
            year='{self.year}', genres='{self.genres}')>"


class Genre(Base):
    """SQL Alchemy Model for Genre."""
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    description = Column(String)

    def __repr__(self):
        return "<Genre(id='{self.id}', description='{self.description}')>"


class Prediction(Base):
    """SQL Alchemy Model for Predictions."""
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime(timezone=True), default=func.now())
    movie_id = Column(Integer, ForeignKey("movie.id"))

    movie = relationship("Movie", foreign_keys=[movie_id], lazy="joined")
    values = relationship("PredictionValue", lazy="joined")

    def __repr__(self):
        return "<Prediction (id='{self.id}', movie='{self.movie}',\
             time_stamp='{self.time_stamp}')>"


class PredictionValue(Base):
    """SQL Alchemy Model for Prediction Value."""
    __tablename__ = 'prediction_value'
    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, ForeignKey("prediction.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))
    score = Column(Float)

    prediction = relationship("Prediction", foreign_keys=[
                              prediction_id], lazy="joined")
    movie = relationship("Movie", foreign_keys=[movie_id], lazy="joined")

    def __repr__(self):
        return "<PredictionValue (id='{self.id}', movie='{self.movie}',\
             score='{self.score}')>"


def seed(session):
    """
    Method to check if database is already seeded.

    Parameters
    ----------
    session : Session
        SqlAlchemy session to be used for seeding the database.
    """
    if session.query(Movie).count() > 0:
        logging.info('Movies table already seeded.')
        return
    seed_movies(session)


def seed_movies(session):
    """
    Mathod to seed the database with movies.

    Parameters
    ----------
    session : Session
        SqlAlchemy session to be used for seeding the database.
    """
    genres = {}
    movies = read_movies()
    for index, movie in enumerate(movies):
        movie_genres = []
        for genre in movie['genres']:
            if genre in genres:
                genre = genres[genre]
            else:
                genre = Genre(description=genre)
                session.add(genre)
                genres[genre.description] = genre
            movie_genres.append(genre)
        session.add(Movie(id=movie['id'], title=movie['title'],
                          year=movie['year'], genres=movie_genres))
        if index % 100 == 1:
            session.commit()
    session.commit()
