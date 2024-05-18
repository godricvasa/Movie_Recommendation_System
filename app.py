import streamlit as st
import pickle 
import pandas as pd
import requests
# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('sim.pkl', 'rb'))

#recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)

    return recommended_movies, recommended_movies_posters

#poster fetching

def fetch_poster(movie_id):
    try:
        response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=9e0cc8829a280563c6f31915396ba0c2".format(movie_id))
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie poster: {e}")
        return None





# Title card
st.title('Movie Recommender System')

# Search bar
selected_movie_name = st.selectbox('Search for your desired movie?', movies['title'].values)

# Button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    if names and posters:
        col1, col2,col3,col4,col5= st.columns(5)

        with col1:
                st.text(names[0])
                st.image(posters[0]) 
        with col2:
                 st.text(names[1])
                 st.image(posters[1]) 
        with col3:
                 st.text(names[2])
                 st.image(posters[2]) 
        with col4:
                 st.text(names[3])
                 st.image(posters[3]) 
        with col5:
                 st.text(names[4])
                 st.image(posters[4])         
   
         

                   
           
            





