import streamlit as st
import requests
import json

genres = {}
default_image = "https://st3.depositphotos.com/1322515/35964/v/450/"\
    "depositphotos_359648638-stock-illustration-image-available-icon.jpg"


def get_movie_image(movie):
    url = f'http://www.omdbapi.com/?t={movie["title"]}&year={movie["year"]}'\
        '&apikey=c9eb1bb2'
    movie_details = json.loads(requests.get(url).text)
    if 'Poster' in movie_details:
        return movie_details['Poster']
    else:
        return default_image


def get_movie_genres(movie):
    return ", ".join([genre["description"] for genre in movie["genres"]])


def print_movie_tiles(movies, callback=None, columns=4, history=True):
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
                container.write('##### Genres')
                container.write(get_movie_genres(movie))
            except Exception:
                container = st.container()
                if callback:
                    button = container.button(
                        'Get Similar Movies', key=movie['id'])
                container.write(f'#### {movie["title"]}')
                container.write(f'##### {movie["year"]}')
                container.image(default_image)
                container.write('##### Genres')
                container.write(get_movie_genres(movie))
        if button:
            callback(movie['id'])
        if index > 20:
            return
