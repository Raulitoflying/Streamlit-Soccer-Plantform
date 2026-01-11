
from io import BytesIO
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

    def _normalize_dataframe(self):
        """
        Normalize team_data into a DataFrame with consistent column order.

        Returns:
            DataFrame: Normalized dataframe or None if no data.
        """
        if not self.team_data:
            return None

        # Preserve first-seen key order across rows
        ordered_keys = []
        for row in self.team_data:
            for key in row.keys():
                if key not in ordered_keys:
                    ordered_keys.append(key)

        return pd.DataFrame(self.team_data)[ordered_keys]

    def export_to_csv(self, filename=None):
        """
        Exports the team data to a CSV file or returns CSV bytes for download.

        Args:
            filename (str | None): Optional path to save CSV. If None, returns bytes for download.

        Returns:
            dict: {success, message, data (optional BytesIO)} for UI handling.
        """
        df = self._normalize_dataframe()
        if df is None:
            return {"success": False, "message": "No data available to export."}

        try:
            if filename:
                df.to_csv(filename, index=False)
                return {"success": True, "message": f"Exported to {filename}", "path": filename}

            # In-memory bytes for Streamlit download
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return {"success": True, "message": "CSV generated.", "data": buffer}
        except Exception as e:
            return {"success": False, "message": f"CSV export error: {e}"}

    def export_to_excel(self, filename=None):
        """
        Exports the team data to an Excel file or returns Excel bytes for download.

        Args:
            filename (str | None): Optional path to save Excel. If None, returns bytes for download.

        Returns:
            dict: {success, message, data (optional BytesIO)} for UI handling.
        """
        df = self._normalize_dataframe()
        if df is None:
            return {"success": False, "message": "No data available to export."}

        try:
            if filename:
                df.to_excel(filename, index=False)
                return {"success": True, "message": f"Exported to {filename}", "path": filename}

            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            return {"success": True, "message": "Excel generated.", "data": buffer}
        except Exception as e:
            return {"success": False, "message": f"Excel export error: {e}"}
