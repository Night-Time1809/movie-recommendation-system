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

df_display = pd.read_csv("display_data.csv", index_col=0)
df_sorted_vote_avg = df_display[df_display.sort_values(by="vote_avg", ascending=False)["vote_count"] >= 15000]
df_sorted_vote_count = df_display.sort_values(by="vote_count", ascending=False)

st.title("🎬 Movie Recommendation System")
st.header("Welcome, Many of movies to discover. Explore now. 🔍")

selected_movie_name = st.selectbox("Search for a movie...", df_display["title"].values)

st.subheader("What's Popular")

tab1, tab2 = st.tabs(["Most vote scores", "Most votes"])

with tab1:
    with st.expander(""):
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        count = 0
        button1 = st.button("Show more..")

        if button1:
            num = 9
        else:
            num = 3
        
        for i in range(num):
            with columns[count]:
                id_ = df_sorted_vote_avg["id"].iloc[i]
                poster_path = search_data(id=id_, word="poster_path")

                st.image(search_picture(poster_path))
                st.text(df_sorted_vote_avg["title"].iloc[i])

                count += 1
                if (i+1)%3 == 0:
                    count = 0

with tab2:
    with st.expander(""):
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        count = 0
        button2 = st.button("Show more...")

        if button2:
            num = 9
        else:
            num = 3

        for i in range(num):
            with columns[count]:
                id_ = df_sorted_vote_count["id"].iloc[i]
                poster_path = search_data(id=id_, word="poster_path")

                st.image(search_picture(poster_path))
                st.text(df_sorted_vote_count["title"].iloc[i])

                count += 1
                if (i+1)%3 == 0:
                    count = 0