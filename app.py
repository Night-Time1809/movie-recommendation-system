import streamlit as st
import numpy as np
import requests
import pandas as pd
from datetime import datetime, time
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache(suppress_st_warning=True)
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

@st.cache(suppress_st_warning=True)
def search_people_id(name, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    try:
        fetch_name = name.replace(" ", "+")
        fetch_id = requests.get(f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={fetch_name}")
        fetch_id = fetch_id.json()
        fetch_id = fetch_id["results"][0]["id"]
    except:
        fetch_id = None

    return fetch_id

@st.cache(suppress_st_warning=True)
def search_picture_people(person_id, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    try:
        fetch_pic = requests.get(f"https://api.themoviedb.org/3/person/{person_id}/images?api_key={api_key}")
        fetch_pic = fetch_pic.json()
        fetch_pic = fetch_pic["profiles"][0]["file_path"]
        fetch_pic = search_picture(poster_path=fetch_pic)
    except:
        fetch_pic = None

    return fetch_pic

@st.cache(suppress_st_warning=True)
def search_cast(movie_id, num_cast=10, api_key="8265bd1679663a7ea12ac168da84d2e8"):
    fetch_ = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}")
    fetch_ = fetch_.json()
    fetch_ = fetch_["cast"]
    cast = []
    character = []
    for i in range(num_cast):
        try:
            cast.append(fetch_[i]["name"])
            character.append(fetch_[i]["character"])
        except:
            continue
    return cast, character

def format_string(string, join_with, space=False):
    string = string.split()
    string = [i.strip("[ ] , \'") for i in string]
    if space:
        for i in range(len(string)):
            for j in range(1,len(string[i])):
                if string[i][j].isupper():
                    string[i] = string[i][:j] + " " + string[i][j:]
    string = join_with.join(string)
    return string

df_display = pd.read_csv("training_data.csv", index_col=0)
st.write(df_display.head())

st.markdown("# 🎬 Movie Recommendation System")
st.markdown("## Welcome, Many of movies to discover. Explore now. 🔍")

movie_name = sorted(df_display["title"].to_list(), key=str.lower)
selected_movie_name = st.selectbox("Search for a movie...", movie_name)
release_year = df_display["release_date"][df_display["title"] == selected_movie_name].iloc[0]
genre = df_display["genre"][df_display["title"] == selected_movie_name].iloc[0]
genre = format_string(string=genre, join_with=", ", space=True)
runtime = df_display["duration"][df_display["title"] == selected_movie_name].iloc[0]
runtime = f"{runtime//60}h {runtime%60}m"
id_ = df_display["id"][df_display["title"] == selected_movie_name].iloc[0]
overview = search_data(id=id_, word="overview")
tagline = search_data(id=id_, word="tagline")
vote_score = df_display["vote_avg"][df_display["title"] == selected_movie_name].iloc[0]
platform = df_display["platform"][df_display["title"] == selected_movie_name].iloc[0]
platform = format_string(string=platform, join_with=" ")
platform = platform.split()
vote_count = df_display["vote_count"][df_display["title"] == selected_movie_name].iloc[0]
director = df_display["crew"][df_display["title"] == selected_movie_name].iloc[0]
director = format_string(string=director, join_with=", ", space=True)
# cast = df_display["cast"][df_display["title"] == selected_movie_name].iloc[0]
# cast = format_string(string=cast, join_with=", ", space=True)
# cast = cast.split(", ")
# cast_id = [search_people_id(name=i) for i in cast]
# cast_pic = [search_picture_people(person_id=i) for i in cast_id]

cast, character = search_cast(movie_id=id_)
cast_id = [search_people_id(name=i) for i in cast]
cast_pic = [search_picture_people(person_id=i) for i in cast_id]
# st.write(cast)
# st.write(character)
# st.write(cast_id)
# st.write(cast_pic)

status = search_data(id=id_, word="status")
language = search_data(id=id_, word="spoken_languages")[0]["english_name"]
budget = search_data(id=id_, word="budget")
revenue = search_data(id=id_, word="revenue")

path_pic_platform = []
for i in platform:
    if i == "netflix":
        path_pic_platform.append("https://www.themoviedb.org/t/p/original/t2yyOv40HZeVlLjYsCsPHnWLk4W.jpg")
    if i == "amazonprime":
        # path_pic_platform.append("https://cdn.lovesavingsgroup.com/logos/amazon-prime.png")
        path_pic_platform.append("https://www.themoviedb.org/t/p/original/emthp39XA2YScoYL1p0sdbAH2WA.jpg")
    if i == "disneyplus":
        # path_pic_platform.append("https://1000logos.net/wp-content/uploads/2021/01/Disney-Plus-logo.jpg")
        path_pic_platform.append("https://www.themoviedb.org/t/p/original/7Fl8ylPDclt3ZYgNbW2t7rbZE9I.jpg")
    if i == "hulu":
        # path_pic_platform.append("https://assetshuluimcom-a.akamaihd.net/h3o/facebook_share_thumb_default_hulu.jpg")
        path_pic_platform.append("image/hulu_logo_3.jpg")

if st.button("Search"):
    with st.container():
        col_detail = st.columns([1,2])
        with col_detail[0]:         
            poster_path = search_data(id=id_, word="poster_path")
            st.image(search_picture(poster_path))
            
        with col_detail[1]:
            st.markdown(f"## {selected_movie_name} ({release_year})")
            st.markdown(f"{genre} • {runtime}")
            tagline = f"*{tagline}*"
            if tagline != "**":
                st.markdown(tagline)
            st.markdown("##### **Overview**")
            st.markdown(f"{overview}")

        st.markdown(f"Now streaming on:")
        col_platform = st.columns([1.4, 1.4, 1.4, 1.4, 3, 3, 5])
        for i in range(len(path_pic_platform)):
            with col_platform[i]:
                st.image(path_pic_platform[i])
        with col_platform[4]:
            st.markdown("**Vote Scores**")
            fig, ax = plt.subplots(figsize=(5, 5))
            # plt.pie([vote_score, 10.0-vote_score], wedgeprops={"width":0.3},
            # startangle=90, colors=['#5DADE2', '#515A5A'])
            plt.pie([vote_score, 10.0-vote_score], wedgeprops={"width":0.3},
            startangle=90, colors=['#21D07A', '#132B18'])
            plt.text(0, 0, f"{round(vote_score*10, 1)}%", ha='center', va='center', fontsize=42, color="white", weight="bold")
            fig.set_facecolor("#0E1117")
            st.pyplot(fig)
        with col_platform[5]:
            st.markdown("**Votes**")
            st.metric(label="", value=vote_count)
        with col_platform[6]:
            st.markdown("**Director**")
            st.markdown(f"{director}")
    
        with st.expander("More detail"):
            st.markdown("#### **Top Billed Cast**")
            num_pic_inrow = 5
            num_row = len(cast) // num_pic_inrow

            for j in range(num_row):
                with st.container():
                    col_cast = st.columns(num_pic_inrow)
                    for i in range(num_pic_inrow):
                        with col_cast[i]:
                            try:
                                st.image(cast_pic[(num_pic_inrow*j)+i])
                            except:
                                st.image("image/unknown_person.png")
                            st.markdown(f"""**{cast[(num_pic_inrow*j)+i]}**     
                            *{character[(num_pic_inrow*j)+i]}*
                            """)
            
            with st.container():
                st.write("\n")
                col_detail = st.columns([1,1,1,1])
                with col_detail[0]:
                    st.markdown("**Status**")
                    st.markdown(f"{status}")

                with col_detail[1]:
                    st.markdown("**Original Language**")
                    st.markdown(f"{language}")

                with col_detail[2]:
                    st.markdown("**Budget**")
                    st.markdown(f"${budget}")

                with col_detail[3]:
                    st.markdown("**Revenue**")
                    st.markdown(f"${revenue}")

        st.markdown("#### Recommendations")
        col_rec = st.columns(3)

        

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

st.markdown("### Analysing")
# Weighted Average
def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()

with st.expander(""):
    try:
        filter_platform_ana, year_ana, vote_score_ana, vote_count_ana = show_col_filter(count=10000000000)

        df_ana = filter(all_data=df_display, platforms=filter_platform_ana, year_range=year_ana, vote_score_range=vote_score_ana, vote_count_range=vote_count_ana, sorted_by="vote_avg")

        st.write(df_ana.describe())

        st.write("year")
        df_group_year = df_ana.groupby("release_date").apply(w_avg, "vote_avg", "vote_count")
        st.write(df_group_year)
        
        st.write("platform")
        st.write(df_ana.groupby("platform").apply(w_avg, "vote_avg", "vote_count"))

        st.write("genre")
        st.write(df_ana.groupby("genre").apply(w_avg, "vote_avg", "vote_count"))

    except:
        pass
