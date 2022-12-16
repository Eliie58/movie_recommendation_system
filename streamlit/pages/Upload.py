import streamlit as st
import requests
import os
import pandas as pd

API_URL = os.environ["API_URL"]

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon='✌️',
    layout="wide",
    initial_sidebar_state="expanded")

st.write('## Click to upload files')
uploaded_file = st.file_uploader("")
if uploaded_file is not None:

    dataframe = pd.read_csv(uploaded_file)

    requests.post(f'{API_URL}/upload',
                  {'ids': dataframe.iloc[:, 0].values})
