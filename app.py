import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "f40d53bafee246e035482446d99f8b06"
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Image"


def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(url)
        data = response.json()

        if data.get('results'):
            for result in data['results']:
                if result.get('poster_path'):
                    return f"https://image.tmdb.org/t/p/w500{result['poster_path']}"
        return PLACEHOLDER_POSTER
    except:
        return PLACEHOLDER_POSTER


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_titles, recommended_posters


# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Title
st.title("🎬 Movie Recommender System ")

# Search bar with icon
selected_movie_name = st.selectbox(
    "🔍 Search or Select a movie:",
    movies['title'].values
)

# Recommend button
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.text(names[idx])
