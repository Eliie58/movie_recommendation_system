import streamlit as st
import requests
import json
from utils.Utils import print_movie_tiles
import os

api_url = os.environ["API_URL"]

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
    params = st.experimental_get_query_params()
    if 'id' in params:
        st.write('## Your movie suggestions are:')
        st.sidebar.markdown("# Suggestions 📖")
        print_history(id=params['id'])
    else:
        st.write('## Some Previous movie Recommendations')
        st.sidebar.markdown("# History 📖")
        print_history()


def print_history(id=None):
    cols = st.columns([1, 4])
    with cols[0]:
        st.write('### The User Picked')
    with cols[1]:
        st.write('### We suggested')
    if id is None:
        history = json.loads(requests.get(
            f'{api_url}/history').text)
    else:
        history = json.loads(requests.get(
            f'{api_url}/history?id={id[0]}').text)
    for movie in history:
        tiles = [movie["movie"]] + [suggestion["movie"]
                                    for suggestion in movie["values"]]
        print_movie_tiles(tiles, columns=5, history=False)


if __name__ == '__main__':
    main()
