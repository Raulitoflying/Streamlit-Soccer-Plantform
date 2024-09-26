"""
app.py from Yixiang Zhou

5001 final project for final submission
"""
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.title('Welcome to World Football Plantform!')

# Text


st.write('Created by Yixiang Zhou')
st.markdown('[My profile ](https://www.linkedin.com/in/yixiang-zhou-1b5040250/)')
st.markdown('[Discover Data API Details ](https://www.football-data.org)')


# insert image
# URL of the online image
image_url = 'https://cdn.pixabay.com/photo/2016/09/18/20/47/football-1678992_1280.jpg'
# Display the image
st.image(image_url, caption='The wonderful football', use_column_width=True)

st.sidebar.title('Widget Section')

# Some descriptions
apilink = '[Football Data](https://www.football-data.org/)'
with st.sidebar.expander('About the project'):
    st.write('The idea behind this project was motivated by my love for football and curiosity for stats. This project uses RESTful API provided by ', apilink)
    st.write("Introduction: This page is divided into two main functions")
    st.write("One is the football database function, which allows you to view the current world's mainstream matches and tournament information")
    st.write("And the other is the football video function, you can watch exciting football video")

if st.sidebar.button('Go to search statistical data page'):
    switch_page("search")

if st.sidebar.button('Go to watch football video page'):
    switch_page("watch")
