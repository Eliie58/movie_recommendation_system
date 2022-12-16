import streamlit as st
import requests
import json
from utils import print_movie_tiles
import os
import pandas as pd

api_url = os.environ["API_URL"]

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon='✌️',
    layout="wide",
    initial_sidebar_state="expanded")

st.write('## Click to upload files')
# uploaded_file = st.file_uploader("Choose a file")
uploaded_file = st.file_uploader("")
if uploaded_file is not None:

    dataframe = pd.read_csv(uploaded_file)

    requests.post('http://localhost:8081/upload', {'ids' : dataframe.iloc[:, 0].values } )

