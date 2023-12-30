import json
import subprocess  # nosec
import sys
import time
import webbrowser
from pathlib import Path

from flask import Flask

app = Flask(__name__)


class ReportGenerationError(Exception):
    """
    Custom exception class that is raised when an error occurs during the generation of a report.

    Example Usage:
    ```python
    try:
        # code that generates a report
    except ReportGenerationError as e:
        print(f"An error occurred while generating the report: {e}")
    ```

    Inherits all methods and fields from the base `Exception` class.
    """

    pass


class PlayerReport:
    def __init__(self, player_username, player_uuid, bans):
        self.player_username = player_username
        self.player_uuid = player_uuid
        self.bans = bans
        self.script_dir = Path(__file__).resolve().parent
        self.frontend_dir = self.script_dir / "SecretFrontend"

    def generate_report(self):
        """
        Generates a report for a player.

        This method constructs a report dictionary based on the player's username, UUID, and bans data.
        The report is then written to a file called "bans.json" and served in a web browser.

        Raises:
            ReportGenerationError: If an error occurs while generating the report.

        Example Usage:
            player_report = PlayerReport(player_username, player_uuid, bans)
            player_report.generate_report()
        """
        try:
            ban_report = self._construct_report_dict()
            self._write_report_to_file(ban_report)
            self._serve_report_and_open_browser()
        except Exception as e:
            raise ReportGenerationError(
                f"An error occurred while generating the report: {e}"
            ) from e

    def _construct_report_dict(self):
        """
        Constructs a dictionary representing a report for a player.

        Returns:
            dict: A dictionary representing the report for the player. It includes the player's username, UUID, bans data, total number of bans, an empty skin URL, and a list of three empty past skins.
        """
        return {
            "username": self.player_username,
            "uuid": self.player_uuid,
            "bans": self.bans,
            "totalbans": len(self.bans),
            "skinurl": "",
            "pastskins": ["", "", ""],
        }

    def _write_report_to_file(self, report_data):
        """
        Write the report data to a JSON file called "bans.json".

        Args:
            report_data (dict): A dictionary representing the report data to be written to the file.

        Returns:
            None

        Raises:
            None

        Example Usage:
            player_report = PlayerReport(player_username, player_uuid, bans)
            player_report._write_report_to_file(report_data)
        """
        bans_file = self.frontend_dir / "bans.json"
        with bans_file.open("w", encoding="utf-8") as bans_json:
            json.dump(report_data, bans_json, indent=4, default=self._to_json)

    def _serve_report_and_open_browser(self):
        """
        Serves a report in a web browser by starting a local server and opening the browser to the report's URL.

        Example Usage:
        player_report = PlayerReport(player_username, player_uuid, bans)
        player_report._serve_report_and_open_browser()

        This code initializes a PlayerReport object with the player's username, UUID, and bans data. Then, it calls the _serve_report_and_open_browser method to generate and serve the report in a web browser.
        """
        frontend_dir = self.frontend_dir.resolve()
        server_cmd = [
            sys.executable,
            "-m",
            "http.server",
            "--bind",
            "127.0.0.1",
            "8000",
        ]
        with subprocess.Popen(
            server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=frontend_dir
        ) as p:  # nosec
            try:
                webbrowser.open(
                    "http://127.0.0.1:8000/index.html", new=2, autoraise=True
                )
                time.sleep(5)
            finally:
                p.terminate()  # Make sure the server is terminated

    def _to_json(self, obj):
        """
        Convert an object to JSON format.

        Args:
            obj (any): The object to be converted to JSON.

        Returns:
            JSON representation of the object if the object has a `to_json` method.
            None if the object does not have a `to_json` method.
        """
        return obj.to_json() if hasattr(obj, "to_json") else None


@app.route("/")
def serve_report_and_open_browser():
    """
    Serves a report in a web browser by opening the browser to a specific URL.

    Example Usage:
    serve_report_and_open_browser()

    Inputs:
    None

    Outputs:
    - Opens a web browser to the specified URL.
    - Returns the string "Server is running".
    """
    webbrowser.open("http://127.0.0.1:5000/index.html", new=2, autoraise=True)
    return "Server is running"


if __name__ == "__main__":
    app.run()
