import streamlit as st
import numpy as np
import requests
import pandas as pd
from datetime import datetime, time

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

@st.cache(suppress_st_warning=True)
def search_picture(poster_path, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    try:
        fetch_pic = "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        fetch_pic = None
    
    return fetch_pic

df_display = pd.read_csv("training_data.csv", index_col=0)

st.markdown("# 🎬 Movie Recommendation System")
st.markdown("## Welcome, Many of movies to discover. Explore now. 🔍")

movie_name = sorted(df_display["title"].to_list(), key=str.lower)
selected_movie_name = st.selectbox("Search for a movie...", movie_name)
if st.button("Search"):
    with st.container():
        col_detail = st.columns(2)
        with col_detail[0]:
            id_ = df_display["id"][df_display["title"] == selected_movie_name].iloc[0]
            
            poster_path = search_data(id=id_, word="poster_path")
            st.image(search_picture(poster_path))
        with col_detail[1]:
            st.markdown(f"## {selected_movie_name}")
        with st.expander("More detail"):
            st.write("detail")

st.markdown("### What's Popular")

def find_platform(platforms, filter_platform):
    in_platforms = False
    for i in filter_platform:
        if i in platforms:
            in_platforms += True
    if in_platforms > 0:
        return True
    else:
        return False

def filter(all_data, platforms, year_range, vote_score_range, vote_count_range, sorted_by):
    filter_data = all_data[all_data["platform"].apply(find_platform, filter_platform=platforms)]
    filter_data = filter_data[(filter_data["release_date"] >= year_range[0]) & (filter_data["release_date"] <= year_range[1])]
    filter_data = filter_data[(filter_data["vote_avg"] >= vote_score_range[0]) & (filter_data["vote_avg"] <= vote_score_range[1])]
    filter_data = filter_data[(filter_data["vote_count"] >= vote_count_range[0]) & (filter_data["vote_count"] <= vote_count_range[1])]
    filter_data = filter_data.sort_values(by=sorted_by, ascending=False)
    return filter_data

def show_col_filter(count):
    col = st.columns(2)
    with col[0]:
        st.write("Streaming platform:")
        netflix = st.checkbox('Netflix', value=True, key=count*1)
        disney_plus = st.checkbox('Disney+', value=True, key=count*2)
        amazon_prime = st.checkbox('Amazon Prime', value=True, key=count*3)
        hulu = st.checkbox('Hulu' , value=True, key=count*4)
    with col[1]:
        st.write("Year:")
        year = st.slider("Select a range of year", 1901, 2023, (2000, 2023), key=count*5)

    st.write(" ")
    col = st.columns(2)
    with col[0]:
        st.write("Vote score:")
        vote_score = st.slider("Select a range of vote score", 0.0, 10.0, (0.0, 10.0), key=count*6)
    with col[1]:
        st.write("Vote count:")
        vote_count = st.slider("Select a range of vote count", 0, 40000, (15000, 40000), key=count*7)

    filter_platform = []
    if netflix:
        filter_platform.append("netflix")
    if disney_plus:
        filter_platform.append("disneyplus")
    if amazon_prime:
        filter_platform.append("amazonprime")
    if hulu:
        filter_platform.append("hulu")
    return filter_platform, year, vote_score, vote_count

def show_col_movies(df, count_):
    col = st.columns(3)
    count = 0
    button1 = st.button("Show more..", key=count_*8)

    if button1:
        num = 9
    else:
        num = 3
        
    for i in range(num):
        with col[count]:
            id_ = df["id"].iloc[i]
            poster_path = search_data(id=id_, word="poster_path")

            st.image(search_picture(poster_path))
            st.text(df["title"].iloc[i])

            count += 1
            if (i+1)%3 == 0:
                count = 0

tab1, tab2 = st.tabs(["Most vote scores", "Most votes"])

with tab1:
    with st.expander(""):
        st.markdown("#### Filter")      
        
        try:
            filter_platform1, year1, vote_score1, vote_count1 = show_col_filter(count=1)

            df_sorted_vote_avg = filter(all_data=df_display, platforms=filter_platform1, year_range=year1, vote_score_range=vote_score1, vote_count_range=vote_count1, sorted_by="vote_avg")

            show_col_movies(df_sorted_vote_avg, count_=1000)
        except:
            pass

with tab2:
    with st.expander(""):
        st.markdown("#### Filter")      
        
        try:
            filter_platform2, year2, vote_score2, vote_count2 = show_col_filter(count=100)

            df_sorted_vote_count = filter(all_data=df_display, platforms=filter_platform2, year_range=year2, vote_score_range=vote_score2, vote_count_range=vote_count2, sorted_by="vote_count")

            show_col_movies(df_sorted_vote_count, count_=20000)
        except:
            pass