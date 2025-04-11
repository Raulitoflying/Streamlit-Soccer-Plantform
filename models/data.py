"""
models_data.py from Yixiang Zhou

5001 final project for final submission
"""
import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FootballDataAPI:
    """
    A class for fetching football-related data from the Football Data API.

    Attributes:
        data1 (list): Placeholder for general data fetched from the API.
        data2 (list): Placeholder for endpoint-specific data fetched from the API.
        data3 (list): Placeholder for new URL version-specific data fetched from the API.
        api_token (str): API token for authentication.
        request_delay (float): Delay between API requests in seconds.
        max_retries (int): Maximum number of retry attempts for failed requests.
        retry_delay (float): Base delay between retry attempts in seconds.

    Methods:
        __init__(_self):
            Initializes an instance of the FootballDataAPI class.

        fetch_data_general(_self):
            Fetches general football-related data from the API.

        fetch_data_from_endpoint(_self, param, comp_dict, svalue):
            Fetches endpoint-specific football-related data from the API.

        fetch_data_from_new_urlversion(_self, param, comp_dict, svalue):
            Fetches new URL version-specific football-related data from the API.
    """
    def __init__(_self):
        """
        Initializes an instance of the FootballDataAPI class.
        """
        _self.data1 = []
        _self.data2 = []
        _self.data3 = []
        _self.api_token = os.getenv('FOOTBALL_DATA_API_KEY')
        _self.request_delay = 1.5  # 1.5 seconds delay between requests
        _self.max_retries = 3      # Maximum retry attempts
        _self.retry_delay = 5.0    # 5 seconds retry delay
        
        if not _self.api_token:
            st.error("Football Data API key not found. Please set "
                     "FOOTBALL_DATA_API_KEY in your .env file.")
            st.stop()

    def _make_request(_self, url, headers, retries=0):
        """
        Makes an API request with rate limiting and error handling.

        Args:
            url (str): The URL to request.
            headers (dict): The headers to include in the request.
            retries (int): Current retry attempt count.

        Returns:
            dict: The JSON response from the API or None if an error occurs.
        """
        # Apply rate limiting delay
        time.sleep(_self.request_delay)
        
        try:
            response = requests.get(url, headers=headers)
            
            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                if retries < _self.max_retries:
                    wait_time = _self.retry_delay * (retries + 1)
                    st.warning(f"Rate limit reached. Waiting {wait_time} "
                               f"seconds...")
                    time.sleep(wait_time)
                    return _self._make_request(url, headers, retries + 1)
                else:
                    st.error("Rate limit reached. Please try again later.")
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
            return _self._make_request(url, headers, retries + 1)
        
        return None

    @st.cache_data(ttl=3600, persist=True)
    def fetch_data_general(_self):
        """
        Fetches general football-related data from the Football Data API.

        Returns:
            list: Fetched data in list format or empty list if error occurs.
        """
        url = "http://api.football-data.org/v2/competitions/"
        headers = {'X-Auth-Token': _self.api_token}
        
        _self.data1 = _self._make_request(url, headers) or []
        return _self.data1

    @st.cache_data(ttl=3600, persist=True)
    def fetch_data_from_endpoint(_self, param, comp_dict, svalue):
        """
        Fetches endpoint-specific football-related data from the API.

        Args:
            param (str): Parameter specifying the endpoint.
            comp_dict (dict): Dictionary containing competition values.
            svalue (str): Selected value.

        Returns:
            list: Fetched data in list format or empty list if error occurs.
        """
        url = (f"http://api.football-data.org/v2/competitions/"
               f"{comp_dict[svalue]}/{param}")
        headers = {'X-Auth-Token': _self.api_token}
        
        _self.data2 = _self._make_request(url, headers) or []
        return _self.data2

    @st.cache_data(ttl=3600, persist=True)
    def fetch_data_from_new_urlversion(_self, param, comp_dict, svalue):
        """
        Fetches new URL version-specific football-related data from the API.

        Args:
            param (str): Parameter specifying the endpoint for the new URL 
                        version.
            comp_dict (dict): Dictionary containing competition values.
            svalue (str): Selected value.

        Returns:
            list: Fetched data in list format or empty list if error occurs.
        """
        url = (f"http://api.football-data.org/v4/competitions/"
               f"{comp_dict[svalue]}/{param}")
        headers = {'X-Auth-Token': _self.api_token}
        
        _self.data3 = _self._make_request(url, headers) or []
        return _self.data3
