"""
tests_show.py from Yixiang Zhou

5001 final project for final submission
"""
import pytest
from unittest.mock import patch
import requests
from models.data import FootballDataAPI


@pytest.fixture
def test_fetch_data_general_success():
    """
    Test the successful fetch of general football data.

    This test uses a mock HTTP GET request to simulate a successful data retrieval
    and checks whether the fetched data is correctly assigned to the 'data1' attribute.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'some_key': 'some_value'}

        footballdataapi.fetch_data_general()
        assert footballdataapi.data1 == {'some_key': 'some_value'}


def test_fetch_data_general_http_error():
    """
    Test handling of HTTP error during general football data retrieval.

    This test uses a mock HTTP GET request to simulate an HTTP error,
    and checks whether the 'data1' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError()

        footballdataapi.fetch_data_general()
        assert footballdataapi.data1 == []


def test_fetch_data_general_connection_error():
    """
    Test handling of connection error during general football data retrieval.

    This test uses a mock HTTP GET request to simulate a connection error,
    and checks whether the 'data1' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        footballdataapi.fetch_data_general()
        assert footballdataapi.data1 == []


def test_fetch_data_general_timeout_error():
    """
    Test handling of timeout error during general football data retrieval.

    This test uses a mock HTTP GET request to simulate a timeout error,
    and checks whether the 'data1' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        footballdataapi.fetch_data_general()
        assert footballdataapi.data1 == []


def test_fetch_data_general_general_error():
    """
    Test handling of general request exception during general football data retrieval.

    This test uses a mock HTTP GET request to simulate a general request exception,
    and checks whether the 'data1' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException()

        footballdataapi.fetch_data_general()
        assert footballdataapi.data1 == []


def test_fetch_data_from_endpoint_success():
    """
    Test the successful fetch of football data from a specific endpoint.

    This test uses a mock HTTP GET request to simulate a successful data retrieval
    and checks whether the fetched data is correctly assigned to the 'data2' attribute.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'some_key': 'some_value'}

        footballdataapi.fetch_data_from_endpoint('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data2 == {'some_key': 'some_value'}


def test_fetch_data_from_endpoint_http_error():
    """
    Test handling of HTTP error during specific football data retrieval.

    This test uses a mock HTTP GET request to simulate an HTTP error,
    and checks whether the 'data2' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError()

        footballdataapi.fetch_data_from_endpoint('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data2 == []


def test_fetch_data_from_endpoint_connection_error():
    """
    Test handling of connection error during specific football data retrieval.

    This test uses a mock HTTP GET request to simulate a connection error,
    and checks whether the 'data2' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        footballdataapi.fetch_data_from_endpoint('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data2 == []


def test_fetch_data_from_endpoint_timeout_error():
    """
    Test handling of timeout error during specific football data retrieval.

    This test uses a mock HTTP GET request to simulate a timeout error,
    and checks whether the 'data2' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        footballdataapi.fetch_data_from_endpoint('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data2 == []


def test_fetch_data_from_endpoint_general_error():
    """
    Test handling of general request exception during specific football data retrieval.

    This test uses a mock HTTP GET request to simulate a general request exception,
    and checks whether the 'data2' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException()

        footballdataapi.fetch_data_from_endpoint('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data2 == []


def test_fetch_data_from_new_urlversion_success():
    """
    Test the successful fetch of football data from a new URL version.

    This test uses a mock HTTP GET request to simulate a successful data retrieval
    and checks whether the fetched data is correctly assigned to the 'data3' attribute.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'some_key': 'some_value'}

        footballdataapi.fetch_data_from_new_urlversion('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data3 == {'some_key': 'some_value'}


def test_fetch_data_from_new_urlversion_http_error():
    """
    Test handling of HTTP error during football data retrieval from a new URL version.

    This test uses a mock HTTP GET request to simulate an HTTP error,
    and checks whether the 'data3' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError()

        footballdataapi.fetch_data_from_new_urlversion('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data3 == []


def test_fetch_data_from_new_urlversion_connection_error():
    """
    Test handling of connection error during football data retrieval from a new URL version.

    This test uses a mock HTTP GET request to simulate a connection error,
    and checks whether the 'data3' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

        footballdataapi.fetch_data_from_new_urlversion('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data3 == []


def test_fetch_data_from_new_urlversion_timeout_error():
    """
    Test handling of timeout error during football data retrieval from a new URL version.

    This test uses a mock HTTP GET request to simulate a timeout error,
    and checks whether the 'data3' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

        footballdataapi.fetch_data_from_new_urlversion('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data3 == []


def test_fetch_data_from_new_urlversion_general_error():
    """
    Test handling of general request exception during football data retrieval from a new URL version.

    This test uses a mock HTTP GET request to simulate a general request exception,
    and checks whether the 'data3' attribute remains an empty list.
    """
    footballdataapi = FootballDataAPI()
    with patch('models.data.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException()

        footballdataapi.fetch_data_from_new_urlversion('some_param', {'some_value': 'test_comp_id'}, 'some_value')
        assert footballdataapi.data3 == []
