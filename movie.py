import pickle
import streamlit as st
import requests
import pandas as pd



import os
import gdown

# File will be downloaded only if it doesn't exist already
if not os.path.exists("similarity.pkl"):
    url = "https://drive.google.com/uc?id=1AelrpVaGn5W9b3VrgkkYj57bfD24AP8i"
    output = "similarity.pkl"
    gdown.download(url, output, quiet=False)

# 🟡 Use your given API key directly here
api_key = "38368e80bf05661616fff95b768a4914"

# 📦 Poster fetch function
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

# 🎯 Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# 🌟 Streamlit App UI
st.header('🎬 Movie Recommender System')

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie to get recommendations:", movie_list)

# Recommendation display
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
