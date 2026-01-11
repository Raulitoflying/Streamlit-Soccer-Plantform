
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
        __init__(self):
            Initializes an instance of the FootballDataAPI class.

        fetch_data_general(self):
            Fetches general football-related data from the API.

        fetch_data_from_endpoint(self, param, comp_dict, svalue):
            Fetches endpoint-specific football-related data from the API.

        fetch_data_from_new_urlversion(self, param, comp_dict, svalue):
            Fetches new URL version-specific football-related data from the API.
    """
    def __init__(self, api_token=None):
        """
        Initializes an instance of the FootballDataAPI class.
        """
        self.data1 = []
        self.data2 = []
        self.data3 = []
        # allow injection for tests; fallback to env var or st.secrets
        self.api_token = (
            api_token
            or os.getenv('FOOTBALL_DATA_API_KEY')
            or (st.secrets.get('FOOTBALL_DATA_API_KEY') if hasattr(st, 'secrets') else None)
        )
        self.request_delay = 1.5  # 1.5 seconds delay between requests
        self.max_retries = 3      # Maximum retry attempts
        self.retry_delay = 5.0    # 5 seconds retry delay

        if not self.api_token:
            st.error("⚠️ Football Data API key not found. Please set FOOTBALL_DATA_API_KEY in env or st.secrets.")

    def _make_request(self, url, headers, retries=0):
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
        time.sleep(self.request_delay)

        try:
            response = requests.get(url, headers=headers, timeout=10)

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                if retries < self.max_retries:
                    wait_time = self.retry_delay * (retries + 1)
                    st.warning(f"⏳ Rate limit reached. Waiting {wait_time} "
                               f"seconds...")
                    time.sleep(wait_time)
                    return self._make_request(url, headers, retries + 1)
                else:
                    st.error("❌ Rate limit reached. Please try again later.")
                    return None

            # Raise exception for any HTTP error
            response.raise_for_status()

            # Return JSON data if successful
            return response.json()

        except requests.exceptions.HTTPError as errh:
            st.error(f"❌ HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            st.error(f"❌ Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            st.error(f"⏱️ Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            st.error(f"❌ Request Error: {err}")

        # If retries available, try again
        if retries < self.max_retries:
            wait_time = self.retry_delay * (retries + 1)
            st.warning(f"🔄 Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            return self._make_request(url, headers, retries + 1)

        return None

    @st.cache_data(ttl=3600)
    def fetch_data_general(_self):
        """
        Fetches general football-related data from the Football Data API.

        Returns:
            list: Fetched data in list format or empty list if error occurs.
        """
        if not _self.api_token:
            st.error("❌ FOOTBALL_DATA_API_KEY is missing; cannot fetch data.")
            return []

        url = "https://api.football-data.org/v4/competitions/"
        headers = {'X-Auth-Token': _self.api_token}

        _self.data1 = _self._make_request(url, headers) or []
        return _self.data1

    @st.cache_data(ttl=3600)
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
        if not _self.api_token:
            st.error("❌ FOOTBALL_DATA_API_KEY is missing; cannot fetch data.")
            return []

        url = (f"https://api.football-data.org/v4/competitions/"
               f"{comp_dict[svalue]}/{param}")
        headers = {'X-Auth-Token': _self.api_token}

        _self.data2 = _self._make_request(url, headers) or []
        return _self.data2

    @st.cache_data(ttl=3600)
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
        if not _self.api_token:
            st.error("❌ FOOTBALL_DATA_API_KEY is missing; cannot fetch data.")
            return []

        url = (f"https://api.football-data.org/v4/competitions/"
               f"{comp_dict[svalue]}/{param}")
        headers = {'X-Auth-Token': _self.api_token}

        _self.data3 = _self._make_request(url, headers) or []
        return _self.data3

    @st.cache_data(ttl=600)
    def fetch_matches(_self, date_from=None, date_to=None, competitions=None,
                      status=None, limit=50, offset=0):
        """
        Fetch matches with optional filters.

        Args:
            date_from (str): YYYY-MM-DD
            date_to (str): YYYY-MM-DD
            competitions (list[str|int]): competition IDs
            status (str): SCHEDULED, LIVE, IN_PLAY, PAUSED, FINISHED, etc.
            limit (int): page size
            offset (int): pagination offset

        Returns:
            dict: API payload or empty dict.
        """
        if not _self.api_token:
            st.error("❌ FOOTBALL_DATA_API_KEY is missing; cannot fetch matches.")
            return {}

        base_url = "https://api.football-data.org/v4/matches"
        params = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "status": status,
            "limit": limit,
            "offset": offset
        }
        if competitions:
            params["competitions"] = ",".join(map(str, competitions))

        # Remove None values to keep query clean
        params = {k: v for k, v in params.items() if v is not None}

        headers = {'X-Auth-Token': _self.api_token}

        response = _self._make_request(f"{base_url}?{requests.compat.urlencode(params)}", headers)
        return response or {}
