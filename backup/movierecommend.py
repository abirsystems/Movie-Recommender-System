import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests

# Fetch movie poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6cb41288966ad746fb4f14a16e73912a"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Load movies dataset
movies = pickle.load(open('movies.pkl', 'rb'))

# Load similarity matrix locally
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_names = movies['title'].values

# UI
st.title("Movie Recommendation System")
option = st.selectbox('Type or Select a movie from the dropdown : ', movies_names)

# Button to get recommendations
if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(option)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
