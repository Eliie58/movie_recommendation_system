"""This module is for utility functions used in the streamlit web app."""
import json
import logging

import requests
import streamlit as st

genres = {}
DEFAULT_IMAGE = "https://st3.depositphotos.com/1322515/35964/v/450/"\
    "depositphotos_359648638-stock-illustration-image-available-icon.jpg"


@st.cache
def get_movie_image(movie):
    """Function to get movie poster URL."""
    logging.info('Getting Movie image for movie %s', movie["title"])
    url = f'http://www.omdbapi.com/?t={movie["title"]}&year={movie["year"]}'\
        '&apikey=c9eb1bb2'
    movie_details = json.loads(requests.get(url, timeout=10).text)
    if 'Poster' in movie_details:
        return movie_details['Poster']
    else:
        return DEFAULT_IMAGE


def get_movie_genres(movie):
    """Function to get comma separated movie genres from a list."""
    return ", ".join([genre["description"] for genre in movie["genres"]])


def print_movie_tiles(movies, callback=None, columns=4, history=True):
    """Function to print movie tiles."""
    if history:
        st.write(
            f'Showing top {20 if len(movies) > 20 else len(movies)} results')
    for index, movie in enumerate(movies):
        button = False
        if index % columns == 0:
            cols = st.columns(columns)
        with cols[index % columns]:
            try:
                container = st.container()
                if callback:
                    button = container.button(
                        'Get Similar Movies', key=movie['id'])
                container.write(f'#### {movie["title"]}')
                container.write(f'##### {movie["year"]}')
                container.image(get_movie_image(movie))
                if 'score' in movie:
                    container.write(f'#### {int(movie["score"] * 100)} %')
                else:
                    container.write('')
                container.write('##### Genres')
                container.write(get_movie_genres(movie))
            except Exception:
                container = st.container()
                if callback:
                    button = container.button(
                        'Get Similar Movies', key=movie['id'])
                container.write(f'#### {movie["title"]}')
                container.write(f'##### {movie["year"]}')
                container.image(DEFAULT_IMAGE)
                container.write('##### Genres')
                container.write(get_movie_genres(movie))
        if button:
            callback(movie['id'])
        if index > 20:
            return
