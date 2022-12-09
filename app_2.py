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

def recommend(movie_id):
    index = id_.index(movie_id)
    rec = rec_dict[index]
    index_rec = []
    id_rec = []
    similarity = []

    for i in rec:
        index_rec.append(i[0])
        similarity.append(i[1])
        id_rec.append(id_[i[0]])
    
    return index_rec, id_rec, similarity

def show_col_filter(key):
    st.write("Streaming platform in Thailand:")
    col = st.columns((1, 1, 2))
    with col[0]:
        netflix = st.checkbox('Netflix', value=True, key=key+1)
        hotstar = st.checkbox('Hotstar', value=True, key=key+2)
        hbo = st.checkbox('HBO Go', value=True, key=key+3)
        amazon = st.checkbox('Amazon Prime Video', value=True, key=key+4)
        iflix = st.checkbox('iflix', value=True, key=key+5)
    with col[1]:
        mubi = st.checkbox('MUBI', value=True, key=key+6)
        netflix_kids = st.checkbox('Netflix Kids', value=True, key=key+7)
        apple = st.checkbox('Apple TV Plus', value=True, key=key+8)
        other_platform = st.checkbox('Other platforms', value=True, key=key+9)
        not_in_TH = st.checkbox('Not available in Thailand', value=True, key=key+10)

    with col[2]:
        st.write("Year:")
        year = st.slider("Select a range of year", 1990, 2022, (2000, 2022), key=key+1+20)

    st.write(" ")
    col = st.columns(2)
    with col[0]:
        st.write("Vote score:")
        vote_score = st.slider("Select a range of vote score", 0.0, 10.0, (0.0, 10.0), key=key+2+20)
    with col[1]:
        st.write("Vote count:")
        vote_count = st.slider("Select a range of vote count", 0, 40000, (3000, 40000), key=key+3+20)

    st.write(" ")
    st.write("Genre:")
    genre = st.multiselect("",
            ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
            "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
            "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"],
            ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
            "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
            "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"],
            label_visibility="collapsed", key=key+4+20)

    st.write(" ")
    st.write("Sort:")
    col = st.columns(2)
    with col[0]:
        order = st.radio("", ("Descending", "Ascending"), key=key+5+20, label_visibility="collapsed", horizontal=True)
    with col[1]:
        shown = st.number_input(f"Number of results", key=key+6+20, value=12)

    platform = []
    if netflix:
        platform.append("Netflix")
    if hotstar:
        platform.append("Hotstar")
    if hbo:
        platform.append("HBO Go")
    if amazon:
        platform.append("Amazon Prime Video")
    if iflix:
        platform.append("iflix")
    if mubi:
        platform.append("MUBI")
    if netflix_kids:
        platform.append("Netflix Kids")
    if apple:
        platform.append("Apple TV Plus")
    if other_platform:
        platform.extend(["Sun Nxt", "DocAlliance Films", "BroadwayHD", "Viu", "GuideDoc", "Magellan TV", "FilmBox+", "WOW Presents Plus", "DOCSVILLE", "Curiosity Stream", "Cultpix", "True Story", "Dekkoo", "Hoichoi", "Argo"])
    if not_in_TH:
        platform.append("not_in_TH")

    if order == "Ascending":
        ascending = True
    elif order == "Descending":
        ascending = False
  
    return platform, year, vote_score, vote_count, genre, ascending, shown

def filter(platforms, year_range, vote_score_range, vote_count_range, genres, sorted_by, ascending=False):
    movie_id_1 = []
    for platform in platforms:
        movie_id_1.extend(platform_TH_dict[platform]["movie_id"])
    movie_id_1 = np.array(movie_id_1)
    movie_id_1 = np.unique(movie_id_1)
    movie_id_1 = movie_id_1.tolist()

    movie_id_2 = []
    for genre in genres:
        movie_id_2.extend(genre_dict[genre]["movie_id"])
    movie_id_2 = np.array(movie_id_2)
    movie_id_2 = np.unique(movie_id_2)
    movie_id_2 = movie_id_2.tolist()

    movie_id = list(set(movie_id_1) & set(movie_id_2))

    filter_data = display_df[display_df["id"].isin(movie_id)]
    filter_data = filter_data[(filter_data["release_date"] >= f"{year_range[0]}-01-01") & (filter_data["release_date"] <= f"{year_range[1]}-12-31")]
    filter_data = filter_data[(filter_data["vote_avg"] >= vote_score_range[0]) & (filter_data["vote_avg"] <= vote_score_range[1])]
    filter_data = filter_data[(filter_data["vote_count"] >= vote_count_range[0]) & (filter_data["vote_count"] <= vote_count_range[1])]
    filter_data = filter_data.sort_values(by=sorted_by, ascending=ascending)

    return filter_data

def show_col_movies(df, num_movie=9):
    num_pic_inrow = 4
    num_row = math.ceil(num_movie / num_pic_inrow)
    movie_id = df["id"].to_list()
    count = 0

    st.write(" ")
    st.markdown(f"1-{num_movie} of {len(df)} results")
    for j in range(num_row):
        try:
            with st.container():
                col_movie = st.columns(num_pic_inrow)
                for i in range(num_pic_inrow):
                    with col_movie[i]:
                        movie_name = display_dict[movie_id[(num_pic_inrow*j)+i]]["title"]
                        poster_path = display_dict[movie_id[(num_pic_inrow*j)+i]]["poster_path"]
                        vote_score = display_dict[movie_id[(num_pic_inrow*j)+i]]["vote_avg"]
                        vote_count = display_dict[movie_id[(num_pic_inrow*j)+i]]["vote_count"]
                        release_date = display_dict[movie_id[(num_pic_inrow*j)+i]]["release_date"]
                        release_date = datetime.strptime(release_date, "%Y-%m-%d").year
                        
                        if type(poster_path) == str:
                            movie_pic = image_path(poster_path=poster_path)
                            st.image(movie_pic)
                        else:
                            movie_pic = blank_image(picture="movie")
                            st.image(movie_pic)

                        st.markdown(f"**{movie_name}** *({release_date})*")
                        st.markdown(f"Score: {vote_score}")
                        st.markdown(f"Vote: {vote_count}")
                        # fig, ax = plt.subplots(figsize=(2, 2))
                        # plt.pie([vote_score, 10.0-vote_score], wedgeprops={"width":0.3},
                        # startangle=90, colors=['#21D07A', '#132B18'])
                        # plt.text(0, 0, f"{round(vote_score*10, 2)}%", ha='center', va='center', fontsize=20, color="white", weight="bold")
                        # fig.set_facecolor("#0E1117")
                        # st.pyplot(fig)

                    count += 1
                    if count == num_movie:
                        break
                    else:
                        continue
        
        except:
            continue

display_dict = pickle.load(open("data/new_data_dict_2.pkl", "rb"))
display_df = pickle.load(open("data/new_data.pkl", "rb"))
display_df["release_date"] = pd.to_datetime(display_df["release_date"])

cast_dict = pickle.load(open("data/cast_movie_detail_dict_2.pkl", "rb"))
genre_dict = pickle.load(open("data/genre_dict.pkl", "rb"))
platform_TH_dict = pickle.load(open("data/platform_TH_dict.pkl", "rb"))
id_ = pickle.load(open("data/id.pkl", "rb"))
rec_dict = pickle.load(open("data/rec_dict.pkl", "rb"))

display_df_rec = display_df.copy()
display_df_rec = display_df_rec.set_index("id")

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
                st.markdown(f"*{tagline}*")
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
        
        col_show = st.columns((3, 1))
        col_show[0].markdown("#### Recommendations")
        show_rec = col_show[1].number_input(f"Show:", value=4)

        index_rec, id_rec, similarity = recommend(movie_id=selected_movie_id)
        rec_df = display_df_rec.loc[id_rec]
        rec_df["similarity"] = similarity
        rec_df.reset_index(inplace=True)
        show_col_movies(rec_df, num_movie=show_rec)


# def show_col_filter(key):
#     st.write("Streaming platform in Thailand:")
#     col = st.columns((1, 1, 2))
#     with col[0]:
#         netflix = st.checkbox('Netflix', value=True, key=key+1)
#         hotstar = st.checkbox('Hotstar', value=True, key=key+2)
#         hbo = st.checkbox('HBO Go', value=True, key=key+3)
#         amazon = st.checkbox('Amazon Prime Video', value=True, key=key+4)
#         iflix = st.checkbox('iflix', value=True, key=key+5)
#     with col[1]:
#         mubi = st.checkbox('MUBI', value=True, key=key+6)
#         netflix_kids = st.checkbox('Netflix Kids', value=True, key=key+7)
#         apple = st.checkbox('Apple TV Plus', value=True, key=key+8)
#         other_platform = st.checkbox('Other platforms', value=True, key=key+9)
#         not_in_TH = st.checkbox('Not available in Thailand', value=True, key=key+10)

#     with col[2]:
#         st.write("Year:")
#         year = st.slider("Select a range of year", 1990, 2022, (2000, 2022), key=key+1+20)

#     st.write(" ")
#     col = st.columns(2)
#     with col[0]:
#         st.write("Vote score:")
#         vote_score = st.slider("Select a range of vote score", 0.0, 10.0, (0.0, 10.0), key=key+2+20)
#     with col[1]:
#         st.write("Vote count:")
#         vote_count = st.slider("Select a range of vote count", 0, 40000, (3000, 40000), key=key+3+20)

#     st.write(" ")
#     st.write("Genre:")
#     genre = st.multiselect("",
#             ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
#             "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
#             "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"],
#             ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
#             "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
#             "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"],
#             label_visibility="collapsed", key=key+4+20)

#     st.write(" ")
#     st.write("Sort:")
#     col = st.columns(2)
#     with col[0]:
#         order = st.radio("", ("Descending", "Ascending"), key=key+5+20, label_visibility="collapsed", horizontal=True)
#     with col[1]:
#         shown = st.number_input(f"Number of results", key=key+6+20, value=12)

#     platform = []
#     if netflix:
#         platform.append("Netflix")
#     if hotstar:
#         platform.append("Hotstar")
#     if hbo:
#         platform.append("HBO Go")
#     if amazon:
#         platform.append("Amazon Prime Video")
#     if iflix:
#         platform.append("iflix")
#     if mubi:
#         platform.append("MUBI")
#     if netflix_kids:
#         platform.append("Netflix Kids")
#     if apple:
#         platform.append("Apple TV Plus")
#     if other_platform:
#         platform.extend(["Sun Nxt", "DocAlliance Films", "BroadwayHD", "Viu", "GuideDoc", "Magellan TV", "FilmBox+", "WOW Presents Plus", "DOCSVILLE", "Curiosity Stream", "Cultpix", "True Story", "Dekkoo", "Hoichoi", "Argo"])
#     if not_in_TH:
#         platform.append("not_in_TH")

#     if order == "Ascending":
#         ascending = True
#     elif order == "Descending":
#         ascending = False
  
#     return platform, year, vote_score, vote_count, genre, ascending, shown

# def filter(platforms, year_range, vote_score_range, vote_count_range, genres, sorted_by, ascending=False):
#     movie_id_1 = []
#     for platform in platforms:
#         movie_id_1.extend(platform_TH_dict[platform]["movie_id"])
#     movie_id_1 = np.array(movie_id_1)
#     movie_id_1 = np.unique(movie_id_1)
#     movie_id_1 = movie_id_1.tolist()

#     movie_id_2 = []
#     for genre in genres:
#         movie_id_2.extend(genre_dict[genre]["movie_id"])
#     movie_id_2 = np.array(movie_id_2)
#     movie_id_2 = np.unique(movie_id_2)
#     movie_id_2 = movie_id_2.tolist()

#     movie_id = list(set(movie_id_1) & set(movie_id_2))

#     filter_data = display_df[display_df["id"].isin(movie_id)]
#     filter_data = filter_data[(filter_data["release_date"] >= f"{year_range[0]}-01-01") & (filter_data["release_date"] <= f"{year_range[1]}-12-31")]
#     filter_data = filter_data[(filter_data["vote_avg"] >= vote_score_range[0]) & (filter_data["vote_avg"] <= vote_score_range[1])]
#     filter_data = filter_data[(filter_data["vote_count"] >= vote_count_range[0]) & (filter_data["vote_count"] <= vote_count_range[1])]
#     filter_data = filter_data.sort_values(by=sorted_by, ascending=ascending)

#     return filter_data

# def show_col_movies(df, num_movie=9):
#     num_pic_inrow = 4
#     num_row = math.ceil(num_movie / num_pic_inrow)
#     movie_id = df["id"].to_list()
#     count = 0

#     st.write(" ")
#     st.markdown(f"1-{num_movie} of {len(df)} results")
#     for j in range(num_row):
#         try:
#             with st.container():
#                 col_movie = st.columns(num_pic_inrow)
#                 for i in range(num_pic_inrow):
#                     with col_movie[i]:
#                         movie_name = display_dict[movie_id[(num_pic_inrow*j)+i]]["title"]
#                         poster_path = display_dict[movie_id[(num_pic_inrow*j)+i]]["poster_path"]
#                         vote_score = display_dict[movie_id[(num_pic_inrow*j)+i]]["vote_avg"]
#                         vote_count = display_dict[movie_id[(num_pic_inrow*j)+i]]["vote_count"]
#                         release_date = display_dict[movie_id[(num_pic_inrow*j)+i]]["release_date"]
#                         release_date = datetime.strptime(release_date, "%Y-%m-%d").year
                        
#                         if type(poster_path) == str:
#                             movie_pic = image_path(poster_path=poster_path)
#                             st.image(movie_pic)
#                         else:
#                             movie_pic = blank_image(picture="movie")
#                             st.image(movie_pic)

#                         st.markdown(f"**{movie_name}** *({release_date})*")
#                         st.markdown(f"Score: {vote_score}")
#                         st.markdown(f"Vote: {vote_count}")
#                         # fig, ax = plt.subplots(figsize=(2, 2))
#                         # plt.pie([vote_score, 10.0-vote_score], wedgeprops={"width":0.3},
#                         # startangle=90, colors=['#21D07A', '#132B18'])
#                         # plt.text(0, 0, f"{round(vote_score*10, 2)}%", ha='center', va='center', fontsize=20, color="white", weight="bold")
#                         # fig.set_facecolor("#0E1117")
#                         # st.pyplot(fig)

#                     count += 1
#                     if count == num_movie:
#                         break
#                     else:
#                         continue
        
#         except:
#             continue
                    

st.markdown("### What's Popular")
tab1, tab2 = st.tabs(["Most vote scores", "Most votes"])
with tab1:
    with st.expander(""):
        st.markdown("#### Filter")
        platform1, year1, vote_score1, vote_count1, genre1, ascending1, shown1 = show_col_filter(key=10)

        df_sorted_vote_avg = filter(platform1, year1, vote_score1, vote_count1, genre1, sorted_by=["vote_avg", "vote_count", "release_date"], ascending=ascending1)

        show_col_movies(df=df_sorted_vote_avg, num_movie=shown1)

with tab2:
    with st.expander(""):
        st.markdown("#### Filter")
        platform2, year2, vote_score2, vote_count2, genre2, ascending2, shown2 = show_col_filter(key=20)

        df_sorted_vote_count = filter(platform2, year2, vote_score2, vote_count2, genre2, sorted_by=["vote_count", "vote_avg", "release_date"], ascending=ascending2)

        show_col_movies(df=df_sorted_vote_count, num_movie=shown2)
