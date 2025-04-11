"""
models_video.py from Yixiang Zhou

5001 final project for final submission
"""
import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ScoreBatVideoAPI:
    """
    A class for accessing the ScoreBat Video API.

    Attributes:
        video_data (list): Placeholder for storing video-related data.
        api_token (str): API token for authentication.
        request_delay (float): Delay between API requests in seconds.
        max_retries (int): Maximum number of retry attempts for failed requests.
        retry_delay (float): Base delay between retry attempts in seconds.

    Methods:
        __init__(_self):
            Initializes an instance of the ScoreBatVideoAPI class.

        get_recent_video(_self):
            Fetches recent feed videos from the ScoreBat Video API.

    """
    def __init__(_self):
        """
        Initializes an instance of the ScoreBatVideoAPI class.
        """
        _self.video_data = []
        _self.api_token = os.getenv('SCOREBAT_API_KEY')
        _self.request_delay = 1.0  # 1 second delay between requests
        _self.max_retries = 3      # Maximum retry attempts
        _self.retry_delay = 3.0    # 3 seconds retry delay
        
        if not _self.api_token:
            st.error("ScoreBat API key not found. Please set "
                     "SCOREBAT_API_KEY in your .env file.")
            st.stop()

    def _make_request(_self, url, retries=0):
        """
        Makes an API request with rate limiting and error handling.

        Args:
            url (str): The URL to request.
            retries (int): Current retry attempt count.

        Returns:
            dict: The JSON response from the API or None if an error occurs.
        """
        # Apply rate limiting delay
        time.sleep(_self.request_delay)
        
        try:
            response = requests.get(url)
            
            # Handle rate limiting or service errors
            if response.status_code in [429, 500, 502, 503, 504]:
                if retries < _self.max_retries:
                    wait_time = _self.retry_delay * (retries + 1)
                    st.warning(f"Service issue or rate limit reached. "
                               f"Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    return _self._make_request(url, retries + 1)
                else:
                    st.error("Service unavailable. Please try again later.")
                    return None
            
            # Raise exception for any HTTP error
            response.raise_for_status()
            
            # Return JSON data if successful
            return response.json()
            
        except requests.exceptions.HTTPError as errh:
            st.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            st.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            st.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            st.error(f"Request Error: {err}")
        
        # If retries available, try again
        if retries < _self.max_retries:
            wait_time = _self.retry_delay * (retries + 1)
            st.warning(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            return _self._make_request(url, retries + 1)
        
        return None

    @st.cache_data(ttl=1800, persist=True)
    def get_recent_video(_self):
        """
        Fetches recent feed videos from the ScoreBat Video API.

        Returns:
            list: Fetched video data in list format or empty list if an error 
                 occurs.
        """
        base_url = "https://www.scorebat.com/video-api/v3/feed/"
        url = f"{base_url}?token={_self.api_token}"
        
        response_data = _self._make_request(url)
        
        if response_data:
            videos_data = response_data.get('response', [])
            return videos_data
        
        return []
