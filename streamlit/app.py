import streamlit as st
import requests

st.set_page_config(
    page_title="Streamlit App",
    page_icon='✌️',
    layout="wide",
    initial_sidebar_state="expanded")


def main():
    st.write('Welcome to Streamlit in Docker')
    st.write(requests.get('http://api:80/').text)


if __name__ == '__main__':
    main()
