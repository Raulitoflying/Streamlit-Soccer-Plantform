"""
pages_watch.py from Yixiang Zhou

5001 final project for final submission
"""
from models.video import ScoreBatVideoAPI
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.title('World Football Game Video')
st.sidebar.title('Widget Section :soccer:')

st.write('Want to watch the amazing football game?')

# insert image
# URL of the online image
image_url = 'https://cdn.pixabay.com/photo/2013/12/12/21/48/football-stadium-227561_1280.jpg'
# Display the image
st.image(image_url, caption='The Wonderful Game', use_column_width=True)

with st.sidebar.expander('About this page'):
    st.write('Click the button below to get the latest and most comprehensive videos and highlights of football matches through our platform!')

if st.sidebar.button('Go back to main page'):
    switch_page("app")


if st.button("Fetch the Highlight video"):
    my_video = ScoreBatVideoAPI()
    video_data = my_video.get_recent_video()

    # List the matches in order
    for video_info in video_data:
        title = video_info.get('title', '')
        competition = video_info.get('competition', '')
        matchview_url = video_info.get('matchviewUrl', '')
        thumbnail = video_info.get('thumbnail', '')
        date = video_info.get('date', '')
        videos = video_info.get('videos', [])

        st.subheader(f"{title} - {competition}")

        # Add contest link
        st.markdown(f"[Watch Match]({matchview_url})", unsafe_allow_html=True)

        st.image(thumbnail, caption=f"Date: {date}", use_column_width=True)

        for video in videos:
            video_title = video.get('title', '')
            embed_code = video.get('embed', '')

            st.subheader(video_title)
            st.markdown(embed_code, unsafe_allow_html=True)
