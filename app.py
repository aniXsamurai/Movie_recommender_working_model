import streamlit as st
import pickle
import requests
import pandas as pd

# Function to fetch poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ec0a1309b1bda015755a57ef2f98343c"
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # ✅ fetch top 10 similar movies (excluding the selected one)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id  # TMDB ID
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))  # Poster URL
    return recommended_movies, recommended_posters


# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

st.title("🎬 Movie Recommender System")

# Movie selection
selected_movie = st.selectbox('Select a movie below', movies_list)

# Show recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    # 🔹 First row (5 movies)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(posters[i])
            st.markdown(f"<h6 style='text-align:center; font-size:14px;'>{names[i]}</h6>", unsafe_allow_html=True)

    # 🔹 Second row (next 5 movies)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(posters[i + 5])
            st.markdown(f"<h6 style='text-align:center; font-size:14px;'>{names[i + 5]}</h6>", unsafe_allow_html=True)
