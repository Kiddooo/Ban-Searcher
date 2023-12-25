import json
import subprocess  # nosec
import sys
import webbrowser
from pathlib import Path

from flask import Flask

app = Flask(__name__)


class ReportGenerationError(Exception):
    pass


class PlayerReport:
    def __init__(self, player_username, player_uuid, bans):
        self.player_username = player_username
        self.player_uuid = player_uuid
        self.bans = bans
        self.script_dir = Path(__file__).resolve().parent
        self.frontend_dir = self.script_dir / "SecretFrontend"

    def generate_report(self):
        try:
            ban_report = self._construct_report_dict()
            self._write_report_to_file(ban_report)
            self._serve_report_and_open_browser()
        except Exception as e:
            raise ReportGenerationError(
                f"An error occurred while generating the report: {e}"
            )

    def _construct_report_dict(self):
        return {
            "username": self.player_username,
            "uuid": self.player_uuid,
            "bans": self.bans,
            "totalbans": len(self.bans),
            "skinurl": "",
            "pastskins": ["", "", ""],
        }

    def _write_report_to_file(self, report_data):
        bans_file = self.frontend_dir / "bans.json"
        with bans_file.open("w", encoding="utf-8") as bans_json:
            json.dump(report_data, bans_json, indent=4, default=self._to_json)

    def _serve_report_and_open_browser(self):
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
                p.wait()  # Wait for the process to terminate
            finally:
                p.terminate()  # Make sure the server is terminated

    def _to_json(self, obj):
        return obj.to_json() if hasattr(obj, "to_json") else None


@app.route("/")
def serve_report_and_open_browser():
    webbrowser.open("http://127.0.0.1:5000/index.html", new=2, autoraise=True)
    return "Server is running"


if __name__ == "__main__":
    app.run()
