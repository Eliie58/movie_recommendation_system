from gc import callbacks
import streamlit as st
import requests
import json
from PIL import Image
from utils.Utils import print_movie_tiles
import webbrowser
import os

genres = {}
default_image = "https://st3.depositphotos.com/1322515/35964/v/450/depositphotos_359648638-stock-illustration-image-available-icon.jpg"
api_url = os.environ["API_URL"]
base_url = os.environ["BASE_URL"]

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon='✌️',
    layout="wide",
    initial_sidebar_state="expanded")


def main():
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
    st.write('## Wondering what new movies to watch?')
    st.write('#### Pick a movie you''ve already watched, and i''ll help you')
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
    movies = json.loads(requests.get(
        f'{api_url}/movies?genre_id={genre}&title={movie_name}').text)
    if len(movies) == 0:
        st.write(
            f'### No {format_func(genre)} movies found with titles similar to {movie_name}')
        return
    print_movie_tiles(movies, callback=predict_movies)


def predict_movies(movie_id):
    pred_id = json.loads(requests.get(
        f'{{api_url}}/single-prediction?movie_id={movie_id}').text)
    webbrowser.open_new_tab(f'{base_url}/History?id={pred_id}')


def get_genres():
    genre_ids = []
    genre_list = json.loads(requests.get(f'{api_url}/genres').text)
    for genre in genre_list:
        id = genre["id"]
        description = genre["description"]
        genre_ids.append(id)
        genres[id] = description
    return genre_ids


def format_func(option):
    return genres[option]


if __name__ == '__main__':
    main()
