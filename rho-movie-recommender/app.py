from urllib import response
import streamlit as st
import pandas as pd
import difflib 
import pickle
import requests

st.title("Movie Recommendation System")

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movie_dict)
option = st.selectbox('Enter/Select the movie you would like recommendations for?', movies['Title'].values)

def get_index():
    matches = difflib.get_close_matches(option, movies['Title'])
    close_match = matches[0]
    movie_index = movies[movies['Title'] == close_match].index.values[0]
    return movie_index

def poster(id):
    response = requests.get("https://www.omdbapi.com/?i=tt" + str(id) + "&apikey=2c4448a0")
    data = response.json()
    return data['Poster']

def recommend(movie):
    similar_movie = sorted(list(enumerate(similarity[get_index()])), reverse=True, key=lambda x: x[1])[1:5]
    recommended_movies = []
    posters = []
    for i in similar_movie:
        id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].Title)
        posters.append(poster(id))
    return recommended_movies, posters

st.write('These movies are similar to ', option)

if st.button('Recommend movies'):
    names, posters = recommend(option)
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    with col1:
        st.caption(names[0])
        st.image(posters[0], use_column_width='always')

    with col2:
        st.caption(names[1])
        st.image(posters[1], use_column_width='always')

    with col3:
        st.caption(names[2])
        st.image(posters[2], use_column_width='always')

    with col4:
        st.caption(names[3])
        st.image(posters[3], use_column_width='always')
    