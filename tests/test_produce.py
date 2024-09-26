"""
tests_produce.py from Yixiang Zhou

5001 final project for final submission
"""
import pandas as pd
import pytest
from models.produce import DataExporter


@pytest.fixture
def sample_team_data():
    """
    Fixture providing sample team data for testing.

    Returns:
        list: Sample team data in dictionary format.
    """
    return [
        {'Team': 'Team A', 'Wins': 10, 'Losses': 5},
        {'Team': 'Team B', 'Wins': 8, 'Losses': 7},
        # Add more team data as needed
    ]


def test_export_to_csv(tmp_path, sample_team_data):
    """
    Test the export_to_excel method of DataExporter.

    Args:
        tmp_path (pytest.fixture): Temporary directory for testing.
        sample_team_data (list): Sample team data for testing.
    """
    # Create an instance of DataExporter
    exporter = DataExporter(sample_team_data)

    # Define the expected CSV file content
    expected_csv_content = "Team,Wins,Losses\nTeam A,10,5\nTeam B,8,7\n"

    # Use tmp_path fixture to create a temporary directory for testing
    tmp_file_path = tmp_path / "test_team_data.csv"

    # Call the export_to_csv method
    exporter.export_to_csv(filename=tmp_file_path)

    # Read the content of the generated CSV file
    with open(tmp_file_path, 'r') as csv_file:
        actual_csv_content = csv_file.read()

    # Assert the content matches the expected CSV content
    assert actual_csv_content == expected_csv_content


def test_export_to_excel(tmp_path, sample_team_data):
    # Create an instance of DataExporter
    exporter = DataExporter(sample_team_data)

    # Define the expected Excel file content
    expected_excel_content = "Team,Wins,Losses\nTeam A,10,5\nTeam B,8,7\n"

    # Use tmp_path fixture to create a temporary directory for testing
    tmp_file_path = tmp_path / "test_team_data.xlsx"

    # Call the export_to_excel method
    exporter.export_to_excel(filename=tmp_file_path)

    # Read the content of the generated Excel file
    actual_excel_content = pd.read_excel(tmp_file_path).to_csv(index=False)

    # Assert the content matches the expected Excel content
    assert actual_excel_content == expected_excel_content
