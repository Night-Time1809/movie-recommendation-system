import streamlit as st
import numpy as np
import requests
import pandas as pd

def search_data(id, word, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    try:
        if id:
            id = int(id)
            fetch_data = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US")
            fetch_data = fetch_data.json()
            fetch_data = fetch_data[word]
        else:
            fetch_data = None
    except:
        fetch_data = None

    return fetch_data

def search_picture(poster_path, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    try:
        fetch_pic = "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        fetch_pic = None
    
    return fetch_pic

df_display = pd.read_csv("")


st.title("🎬 Movie Recommendation System")
st.header("Welcome, Many of movies to discover. Explore now. 🔍")

st.subheader("What's Popular")

tab1, tab2 = st.tabs(["Most vote scores", "Most votes"])

with tab1:
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    for col in columns:
        with col:
            st.image("https://static.streamlit.io/examples/cat.jpg")
            st.text("Movie name")

with tab2:
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    for col in columns:
        with col:
            st.image("https://static.streamlit.io/examples/dog.jpg")
            st.text("Movie name")
