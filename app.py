import streamlit as st
import pickle
import pandas as pd
import requests

with open("static/styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def feth_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=194f2f32edc6b9c9d3cfbd6c9831ec40&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    if movie not in movies['title'].values:
        st.warning(f"{movie} not found in the DataFrame.")
        return

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_tags = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(feth_poster(movie_id))
        recommended_movies_tags.append(movies.iloc[i[0]].tags)

    return recommended_movies, recommended_movies_posters, recommended_movies_tags


st.title("Movies Recommender System")

selected_movie_name = st.selectbox(
    'Pick a movie for recommendation',
    movies['title'].values)

if st.button('Recommend'):
    names, posters, tags = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.write("Tags:", tags[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.write("Tags:", tags[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.write("Tags:", tags[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.write("Tags:", tags[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.write("Tags:", tags[4])
