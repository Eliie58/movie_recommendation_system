# pylint: disable=E1101
"""This module is the Home page for streamlit web application."""

import json
import os
import webbrowser
import logging

import requests
from utils import print_movie_tiles
import streamlit as st


genres = {}
api_url = os.environ["API_URL"]
base_url = os.environ["BASE_URL"]

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon='✌️',
    layout="wide",
    initial_sidebar_state="expanded")


def main():
    """Main function to display the Home"""
    hide_img_fs = '''
    <style>
        button[title="View fullscreen"] {
            visibility: hidden;
        }
        .css-eczf16.e16nr0p31 {
            visibility: hidden;
        }
    </style>
    '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)
    st.write("## Wondering what new movies to watch?")
    st.write("#### Pick a movie you''ve already watched, and i''ll help you")
    cols = st.columns([2, 1])
    with cols[0]:
        genre = st.selectbox("Select the movie genre", options=get_genres(),
                             format_func=format_func)
    with cols[1]:
        movie_name = st.text_input(
            "Enter the movie name",
            placeholder="Enter the movie name",
        )
    print_movies(genre, movie_name)


def print_movies(genre, movie_name):
    """Function to fetch and print movies."""
    movies = json.loads(requests.get(
        f'{api_url}/movies?genre_id={genre}&title={movie_name}',
        timeout=10).text)
    if len(movies) == 0:
        st.write(
            f'### No {format_func(genre)} movies found with titles similar'
            ' to {movie_name}')
        return
    print_movie_tiles(movies, callback=predict_movies)


def predict_movies(movie_id):
    """
    Function to predict similar movies,
    and open a new tab with the results.
    """
    prediction = json.loads(requests.get(
        f'{api_url}/single-prediction?movie_id={movie_id}', timeout=10).text)
    webbrowser.open_new_tab(f'{base_url}/History?id={prediction["id"]}')


def get_genres():
    """Function to get all genre ids."""
    genre_ids = []
    genre_list = json.loads(requests.get(f'{api_url}/genres', timeout=10).text)
    for genre in genre_list:
        genre_id = genre["id"]
        description = genre["description"]
        genre_ids.append(genre_id)
        genres[genre_id] = description
    return genre_ids


def format_func(option):
    """Function to get Genre Name from Id."""
    return genres[option]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
