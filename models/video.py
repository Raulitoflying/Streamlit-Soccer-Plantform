"""
models_video.py from Yixiang Zhou

5001 final project for final submission
"""
import requests
import streamlit as st


class ScoreBatVideoAPI:
    """
    A class for accessing the ScoreBat Video API.

    Attributes:
        video_data (list): Placeholder for storing video-related data.

    Methods:
        __init__(self):
            Initializes an instance of the ScoreBatVideoAPI class.

        get_recent_video(self):
            Fetches recent feed videos from the ScoreBat Video API.

    """
    def __init__(_self):
        """
        Initializes an instance of the ScoreBatVideoAPI class.
        """
        _self.video_data = []

    @st.cache_data(persist=True)
    def get_recent_video(_self):
        """
        Fetches recent feed videos from the ScoreBat Video API.

        Returns:
            list: Fetched video data in list format.
        """
        url = "https://www.scorebat.com/video-api/v3/feed/?token=[MTMxNjgyXzE3MDA3ODA5NzNfMTNkM2M0N2Q1MGI0Mzc1YTEwNTAzOGVjYjRlNDllY2FiYTdlM2QxOA==]"

        try:
            response = requests.get(url)
            response.raise_for_status()
            videos_data = response.json().get('response', [])
            return videos_data

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)
