"""
This module is streamlit page for showing Prediction History
"""

import json
import os

import requests
import streamlit as st

from utils import print_movie_tiles

api_url = os.environ["API_URL"]

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon='✌️',
    layout="wide",
    initial_sidebar_state="expanded")


def main():
    """
    This function is used to create the structure of the webpage.
    """

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
    params = st.experimental_get_query_params()
    if 'id' in params:
        st.write('## Your movie suggestions are:')
        st.sidebar.markdown("# Suggestions 📖")
        print_history(prediction_id=params['id'])
    else:
        st.write('## Some Previous movie Recommendations')
        st.sidebar.markdown("# History 📖")
        print_history()


def print_history(prediction_id=None):
    """
    Function to print the movie preidction history.

    Parameters
    ----------
    prediction_id: int, optional
        The id of the prediction to print
    """

    cols = st.columns([1, 4])
    with cols[0]:
        st.write('### The User Picked')
    with cols[1]:
        st.write('### We suggested')
    if prediction_id is None:
        history = json.loads(requests.get(
            f'{api_url}/history', timeout=10).text)
    else:
        history = json.loads(requests.get(
            f'{api_url}/history?prediction_id={prediction_id[0]}',
            timeout=10).text)
    for movie in history:
        tiles = [movie["movie"]] + sorted([build_movie(suggestion)
                                           for suggestion in movie["values"]],
                                          key=lambda x: x['score'])[::-1]
        print_movie_tiles(tiles, columns=5, history=False)


def build_movie(suggestion):
    """
    Function to bundle movie with score.
    """
    movie = suggestion["movie"]
    movie["score"] = suggestion["score"]
    return movie


if __name__ == '__main__':
    main()
