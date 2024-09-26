"""
models_produce.py from Yixiang Zhou

5001 final project for final submission
"""
import csv
import pandas as pd


class DataExporter:
    """
    A class for exporting team-specific statistics or performance charts.

    Attributes:
        team_data (list): List containing team-specific data in dictionary format.

    Methods:
        __init__(self, team_data):
            Initializes the DataExporter with team-specific data.

        export_to_csv(self, filename="team_data.csv"):
            Exports the team data to a CSV file.

        export_to_excel(self, filename="team_data.xlsx"):
            Exports the team data to an Excel file.
    """
    def __init__(self, team_data):
        """
        Initializes the DataExporter with team-specific data.

        Args:
            team_data (list): List containing team-specific data in dictionary format.
        """
        # Team data passed in at initialization
        self.team_data = team_data

    def export_to_csv(self, filename="team_data.csv"):
        """
        Exports the team data to a CSV file.

        Args:
            filename (str, optional): Name of the CSV file. Defaults to "team_data.csv".
        """
        try:
            # Open CSV file, use newline='' to prevent blank lines
            with open(filename, 'w', newline='') as csvfile:
                # Create CSV write objects
                csv_writer = csv.writer(csvfile)

                # Write to table header
                csv_writer.writerow(self.team_data[0].keys())

                # Write data line by line
                for row in self.team_data:
                    csv_writer.writerow(row.values())

            print(f"Data exported to {filename} successfully.")
        except Exception as e:
            print(f"Error during CSV export: {e}")

    def export_to_excel(self, filename="team_data.xlsx"):
        """
        Exports the team data to an Excel file.

        Args:
            filename (str, optional): Name of the Excel file. Defaults to "team_data.xlsx".
        """
        try:
            # Creating a DataFrame with Pandas
            dataframe = pd.DataFrame(self.team_data)

            # Exporting a DataFrame to an Excel file
            dataframe.to_excel(filename, index=False)

            print(f"Data exported to {filename} successfully.")
        except Exception as e:
            print(f"Error during Excel export: {e}")
