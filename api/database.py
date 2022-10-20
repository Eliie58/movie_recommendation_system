from ast import For
from sqlite3 import Date
from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
import os
from .Utils import readMovies

db_instance = None


class Database():
    engine = db.create_engine(os.environ["DATABASE_URL"])

    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")
        try:
            seed(Session(bind=self.connection))
        except Exception as e:
            print(f'Error {e}')

    def fetch_movies(self):
        self.session = Session(bind=self.connection)
        return self.session.query(Movie).all()

    def fetch_movies_by_genre(self, genre_id, title):
        self.session = Session(bind=self.connection)
        return self.session.query(Movie).filter(Movie.title.ilike("%{}%".format(title))).filter(
            Movie.genres.any(id=genre_id)).order_by(Movie.year.desc()).all()

    def fetch_genres(self):
        self.session = Session(bind=self.connection)
        return self.session.query(Genre).all()

    def fetch_predictions(self, id, n):
        self.session = Session(bind=self.connection)
        if id == 0:
            return self.session.query(Prediction).order_by(Prediction.time_stamp.desc()).limit(10).all()
        else:
            return self.session.query(Prediction).filter(Prediction.id == id).all()

    def store_prediction(self, movie_id, predictions):
        session = Session(bind=self.engine.connect())
        prediction = Prediction(movie_id=movie_id)
        session.add(prediction)
        session.commit()
        for pred in predictions:
            pred_value = PredictionValue(
                movie_id=pred.id, prediction_id=prediction.id)
            session.add(pred_value)
        session.commit()
        return prediction.id

    @staticmethod
    def instance():
        global db_instance
        if db_instance is None:
            db_instance = Database()
        return db_instance


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
        return "<Movie(id='%s', title='%s', year='%s', genres='%s')>" % (self.id, self.title, self.year, self.genres)


class Genre(Base):
    """SQL Alchemy Model for Genre."""
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    description = Column(String)

    def __repr__(self):
        return "<Genre(id='%s', description='%s')>" % (self.id, self.description)


class Prediction(Base):
    """SQL Alchemy Model for Predictions."""
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True)
    time_stamp = Column(DateTime(timezone=True), default=func.now())
    movie_id = Column(Integer, ForeignKey("movie.id"))

    movie = relationship("Movie", foreign_keys=[movie_id], lazy="joined")
    values = relationship("PredictionValue", lazy="joined")

    def __repr__(self):
        return "<Prediction (id='%s', movie='%s', time_stamp='%s')>" % (self.id, self.movie, self.time_stamp)


class PredictionValue(Base):
    """SQL Alchemy Model for Prediction Value."""
    __tablename__ = 'prediction_value'
    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, ForeignKey("prediction.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))

    prediction = relationship("Prediction", foreign_keys=[
                              prediction_id], lazy="joined")
    movie = relationship("Movie", foreign_keys=[movie_id], lazy="joined")

    def __repr__(self):
        return "<PredictionValue (id='%s', movie='%s')>" % (self.id, self.movie)


def seed(session):
    if session.query(Movie).count() > 0:
        print('Movies table already seeded.')
        return
    seed_movies(session)


def seed_movies(session):
    genres = {}
    movies = readMovies()
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
