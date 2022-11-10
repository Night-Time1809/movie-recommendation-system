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

# if st.button("Filter"):
    #     col_1, col_2, col_3 = st.columns(3)
    #     with col_1:
    #         st.write("Streaming platform:")
    #         netflix = st.checkbox('Netflix')
    #         disney_plus = st.checkbox('Disney+')
    #         amazon_prime = st.checkbox('Amazon Prime')
    #         hulu = st.checkbox('Hulu')
    #     with col_2:
    #         st.write("Vote score range:")
    #         values = st.slider("Select a range of vote score", 0.0, 10.0)
    # else:
    #     st.write("no")

with tab1:
    with st.expander(""):
        if st.button("Filter"):
            col = st.columns(2)
            with col[0]:
                st.write("Streaming platform:")
                netflix = st.checkbox('Netflix', value=True)
                disney_plus = st.checkbox('Disney+', value=True)
                amazon_prime = st.checkbox('Amazon Prime', value=True)
                hulu = st.checkbox('Hulu' , value=True)
            with col[1]:
                st.write("Year:")
                values = st.slider("Select a range of year", 1995, 2020, (1995, 2020))

            st.write(" ")
            col = st.columns(2)
            with col[0]:
                st.write("Vote score:")
                values = st.slider("Select a range of vote score", 0.0, 10.0, (0.0, 10.0))
            with col[1]:
                st.write("Vote count:")
                values = st.slider("Select a range of vote count", 0.0, 10.0, (0.0, 10.0))
        # else:
        #     st.write("no")
        # st.write("**Filter**")
        # col = st.columns(3)
        # with col[0]:
        #     st.write("Streaming platform:")
        #     netflix = st.checkbox('Netflix')
        #     disney_plus = st.checkbox('Disney+')
        #     amazon_prime = st.checkbox('Amazon Prime')
        #     hulu = st.checkbox('Hulu')

        col = st.columns(3)
        count = 0
        button1 = st.button("Show more..")

        if button1:
            num = 9
        else:
            num = 3
        
        for i in range(num):
            with col[count]:
                id_ = df_sorted_vote_avg["id"].iloc[i]
                poster_path = search_data(id=id_, word="poster_path")

                st.image(search_picture(poster_path))
                st.text(df_sorted_vote_avg["title"].iloc[i])

                count += 1
                if (i+1)%3 == 0:
                    count = 0

with tab2:
    with st.expander(""):
        col = st.columns(3)
        count = 0
        button2 = st.button("Show more...")

        if button2:
            num = 9
        else:
            num = 3

        for i in range(num):
            with col[count]:
                id_ = df_sorted_vote_count["id"].iloc[i]
                poster_path = search_data(id=id_, word="poster_path")

                st.image(search_picture(poster_path))
                st.text(df_sorted_vote_count["title"].iloc[i])

                count += 1
                if (i+1)%3 == 0:
                    count = 0

# st.subheader('Datetime slider')

# start_time = st.slider(
#      "When do you start?",
#      value=datetime(2020),
#      format="YY")
# st.write("Start time:", start_time)

# st.subheader('Range time slider')

# appointment = st.slider(
#      "Schedule your appointment:",
#      value=(time(11, 30), time(12, 45)))
# st.write("You're scheduled for:", appointment)
st.write("Vote score range:")
values = st.slider("Select a range of vote score", 2000, 2020, (2000, 2020))