import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from datetime import datetime, time
import math

@st.cache(suppress_st_warning=True)
def image_path(poster_path):
    return f"https://image.tmdb.org/t/p/w500{poster_path}"

@st.cache(suppress_st_warning=True)
def blank_image(picture="movie"):
    if picture == "person":
        pic_path = "image/unknown_person.png"
    else:
        pic_path = "image/unknown_movie.png"
    return pic_path

display_dict = pickle.load(open("data/new_data_dict_2.pkl", "rb"))
display_df = pickle.load(open("data/new_data.pkl", "rb"))
display_df["release_date"] = pd.to_datetime(display_df["release_date"])

cast_dict = pickle.load(open("data/cast_movie_detail_dict_2.pkl", "rb"))

st.markdown("# 🎬 Movie Recommendation System")
st.markdown("## Welcome, Many of movies to discover. Explore now. 🔍")

movie_name = sorted(display_df.drop_duplicates(subset="title")["title"].to_list(), key=str.lower)
duplicated_movie_name = display_df[display_df.duplicated(subset="title")]
selected_movie_name = st.selectbox("Search for a movie...", movie_name)

if selected_movie_name in duplicated_movie_name["title"].to_list():
    release_date = display_df["release_date"][display_df["title"] == selected_movie_name]
    release_date = release_date.sort_values(ascending=True)
    selected_date = st.radio("Release date:", release_date.dt.strftime('%d-%m-%Y'), horizontal=True)
    selected_date = datetime.strptime(selected_date, '%d-%m-%Y')
    selected_movie_id = (display_df["id"][(display_df["title"] == selected_movie_name) & (display_df["release_date"] == selected_date)]).iloc[0]
else:
    selected_movie_id = (display_df["id"][display_df["title"] == selected_movie_name]).iloc[0]
    
if st.button("Search"):
    with st.container():
        col_detail = st.columns([1, 2])
        with col_detail[0]:
            if type(display_dict[selected_movie_id]["poster_path"]) == str:
                movie_pic = image_path(poster_path=display_dict[selected_movie_id]["poster_path"])
                st.image(movie_pic)
            else:
                movie_pic = blank_image(picture="movie")
                st.image(movie_pic)

        with col_detail[1]:
            selected_movie_name = display_dict[selected_movie_id]["title"]
            release_year = datetime.strptime(display_dict[selected_movie_id]["release_date"], "%Y-%m-%d").year
            genre = ", ".join(list(display_dict[selected_movie_id]["genre"].values()))
            runtime = display_dict[selected_movie_id]["runtime"]
            if runtime > 60:
                runtime = f"{runtime//60}h {runtime%60}m"
            else:
                runtime = f"{runtime%60}m"
            tagline = display_dict[selected_movie_id]["tagline"]
            overview = display_dict[selected_movie_id]["overview"]

            st.markdown(f"## {selected_movie_name} ({release_year})")
            st.markdown(f"{genre} • {runtime}")
            if type(tagline) == str:
                st.markdown(tagline)
            if type(overview) == str:
                st.markdown("##### **Overview**")
                st.markdown(f"{overview}")

        st.markdown(f"Now streaming on:")
        col_platform = st.columns([1.4, 1.4, 1.4, 1.4, 3, 3, 5])

        with col_platform[4]:
            vote_score = display_dict[selected_movie_id]["vote_avg"]
            
            st.markdown("**Vote Scores**")
            fig, ax = plt.subplots(figsize=(5, 5))
            plt.pie([vote_score, 10.0-vote_score], wedgeprops={"width":0.3},
            startangle=90, colors=['#21D07A', '#132B18'])
            plt.text(0, 0, f"{round(vote_score*10, 1)}%", ha='center', va='center', fontsize=42, color="white", weight="bold")
            fig.set_facecolor("#0E1117")
            st.pyplot(fig)

        with col_platform[5]:
            vote_count = display_dict[selected_movie_id]["vote_count"]

            st.markdown("**Votes**")
            vote_count = "{:,}".format(vote_count)
            st.metric(label="", value=vote_count)

        with col_platform[6]:
            director = ", ".join(list(display_dict[selected_movie_id]["director"].values()))
            st.markdown("**Director**")
            st.markdown(f"{director}")

        with st.expander("More detail"):
            cast_id = list(display_dict[selected_movie_id]["cast"].keys())           

            st.markdown("#### **Top Billed Cast**")
            num_pic_inrow = 5
            num_row = math.ceil(len(cast_id) / num_pic_inrow)
            
            for j in range(num_row):
                try:
                    with st.container():
                        col_cast = st.columns(num_pic_inrow)
                        for i in range(num_pic_inrow):
                            with col_cast[i]:
                                cast_name = cast_dict[cast_id[(num_pic_inrow*j)+i]]["name"]
                                movie_details = cast_dict[cast_id[(num_pic_inrow*j)+i]]["movie_details"]
                                for k in range(len(movie_details)):
                                    if movie_details[k]["movie_id"] == selected_movie_id:
                                        character = movie_details[k]["character"]

                                if cast_dict[cast_id[(num_pic_inrow*j)+i]]["profile_path"]:
                                    cast_pic = image_path(poster_path=cast_dict[cast_id[(num_pic_inrow*j)+i]]["profile_path"])
                                    st.image(cast_pic)
                                else:
                                    cast_pic = blank_image(picture="person")
                                    st.image(cast_pic)
                                if character:
                                    st.markdown(f"""**{cast_name}**     
                                    *{character}*
                                    """)
                                else:
                                    st.markdown(f"**{cast_name}**")
                except:
                    continue

            with st.container():
                status = display_dict[selected_movie_id]["status"]
                language = ", ".join(list(display_dict[selected_movie_id]["language"].values()))
                budget = display_dict[selected_movie_id]["budget"]
                revenue = display_dict[selected_movie_id]["revenue"]

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
                    if budget > 0:
                        st.markdown("${:,.2f}".format(budget))
                    else:
                        st.markdown("")

                with col_detail[3]:
                    st.markdown("**Revenue**")
                    st.markdown("${:,.2f}".format(revenue))

        st.markdown("#### Recommendations")
        col_rec = st.columns(3)


st.markdown("### What's Popular")

