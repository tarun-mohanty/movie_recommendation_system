import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, number_of_movies):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:number_of_movies+1]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies_dic = pickle.load(open('movies_dic.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dic)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
number_of_movies = st.selectbox(
    "Select number of movies to recommended",
    list(range(1,11))
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie,number_of_movies)
    col_list1 = st.columns(4)
    count = 0

    for i in range(len(col_list1)):
        if(count < number_of_movies) :
            with col_list1[i]:
                st.text(recommended_movie_names[count])
                st.image(recommended_movie_posters[count])
                count += 1

    col_list2 = st.columns(4)
    for i in range(len(col_list2)):
        if (count < number_of_movies):
            with col_list2[i]:
                st.text(recommended_movie_names[count])
                st.image(recommended_movie_posters[count])
                count += 1
    col_list3 = st.columns(4)
    for i in range(len(col_list3)):
        if (count < number_of_movies):
            with col_list3[i]:
                st.text(recommended_movie_names[count])
                st.image(recommended_movie_posters[count])
                count += 1



