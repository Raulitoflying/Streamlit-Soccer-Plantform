"""
models_data.py from Yixiang Zhou

5001 final project for final submission
"""
import requests
import streamlit as st


class FootballDataAPI:
    """
    A class for fetching football-related data from the Football Data API.

    Attributes:
        data1 (list): Placeholder for general data fetched from the API.
        data2 (list): Placeholder for endpoint-specific data fetched from the API.
        data3 (list): Placeholder for new URL version-specific data fetched from the API.

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
    def __init__(_self):
        """
        Initializes an instance of the FootballDataAPI class.
        """
        _self.data1 = []
        _self.data2 = []
        _self.data3 = []

    @st.cache_data(persist=True)
    def fetch_data_general(_self):
        """
        Fetches general football-related data from the Football Data API.

        Returns:
            list: Fetched data in list format.
        """
        try:
            url = "http://api.football-data.org/v2/competitions/"
            headers = {'X-Auth-Token': '0f34aeca78bb459d8a663097a3eb0ddf'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                _self.data1 = response.json()
                return _self.data1
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)


    @st.cache_data(persist=True)
    def fetch_data_from_endpoint(_self, param, comp_dict, svalue):
        """
        Fetches endpoint-specific football-related data from the Football Data API.

        Args:
            param (str): Parameter specifying the endpoint.
            comp_dict (dict): Dictionary containing competition values.
            svalue (str): Selected value.

        Returns:
            list: Fetched data in list format.
        """
        try:
            url = f"http://api.football-data.org/v2/competitions/{comp_dict[svalue]}/{param}"
            headers = {'X-Auth-Token': '0f34aeca78bb459d8a663097a3eb0ddf'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                _self.data2 = response.json()
                return _self.data2
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)

    @st.cache_data(persist=True)
    def fetch_data_from_new_urlversion(_self, param, comp_dict, svalue):
        """
        Fetches new URL version-specific football-related data from the Football Data API.

        Args:
            param (str): Parameter specifying the endpoint for the new URL version.
            comp_dict (dict): Dictionary containing competition values.
            svalue (str): Selected value.

        Returns:
            list: Fetched data in list format.
        """
        try:
            url = f"http://api.football-data.org/v4/competitions/{comp_dict[svalue]}/{param}"
            headers = {'X-Auth-Token': '0f34aeca78bb459d8a663097a3eb0ddf'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                _self.data3 = response.json()
                return _self.data3
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong:", err)
