CREATE DATABASE movies;

GRANT ALL PRIVILEGES ON DATABASE movies TO fastapi;

\c movies;

SET
    search_path = public;

CREATE TABLE MOVIE (
    ID NUMERIC,
    TITLE TEXT,
    YEAR NUMERIC
);

CREATE TABLE GENRE (ID SERIAL PRIMARY KEY, DESCRIPTION TEXT);

CREATE TABLE MOVIE_GENRE (
    ID SERIAL PRIMARY KEY,
    MOVIE_ID NUMERIC,
    GENRE_ID NUMERIC
);

CREATE TABLE PREDICTION (
    ID SERIAL PRIMARY KEY,
    MOVIE_ID NUMERIC,
    TIME_STAMP TIMESTAMP
);

CREATE TABLE PREDICTION_VALUE (
    ID SERIAL PRIMARY KEY,
    PREDICTION_ID NUMERIC,
    MOVIE_ID NUMERIC,
    SCORE NUMERIC
);