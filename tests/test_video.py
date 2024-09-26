"""
tests_video.py from Yixiang Zhou

5001 final project for final submission
"""
import pytest
import requests
from unittest.mock import patch
from models.video import ScoreBatVideoAPI


@pytest.fixture
def test_get_recent_video_success():
    """
    Test the successful retrieval of recent video data.

    This test uses a mock HTTP GET request to simulate a successful response,
    and checks whether the 'video_data' attribute is correctly updated.
    """
    video = ScoreBatVideoAPI()
    with patch('models.video.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'response': [{'video_data': 'example'}]}

    video.get_recent_video()
    assert video.video_data == [{'video_data': 'example'}]


def test_get_recent_video_http_error():
    """
    Test handling of HTTP error during recent video retrieval.

    This test uses a mock HTTP GET request to simulate an HTTP error,
    and checks whether the 'video_data' attribute remains an empty list.
    """
    video = ScoreBatVideoAPI()
    with patch('models.video.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError()

    video.get_recent_video()
    assert video.video_data == []


def test_get_recent_video_connection_error():
    """
    Test handling of connection error during recent video retrieval.

    This test uses a mock HTTP GET request to simulate a connection error,
    and checks whether the 'video_data' attribute remains an empty list.
    """
    video = ScoreBatVideoAPI()
    with patch('models.video.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()

    video.get_recent_video()
    assert video.video_data == []


def test_get_recent_video_timeout_error():
    """
    Test handling of timeout error during recent video retrieval.

    This test uses a mock HTTP GET request to simulate a timeout error,
    and checks whether the 'video_data' attribute remains an empty list.
    """
    video = ScoreBatVideoAPI()
    with patch('models.video.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()

    video.get_recent_video()
    assert video.video_data == []


def test_get_recent_video_general_error():
    """
    Test handling of general request exception during recent video retrieval.

    This test uses a mock HTTP GET request to simulate a general request exception,
    and checks whether the 'video_data' attribute remains an empty list.
    """
    video = ScoreBatVideoAPI()
    with patch('models.video.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException()

    video.get_recent_video()
    assert video.video_data == []
