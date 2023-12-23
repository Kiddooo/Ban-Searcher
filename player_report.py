import json
import os
import subprocess #nosec
import sys
import time
import webbrowser

class PlayerReport:
    def __init__(self, player_username, player_uuid, bans):
        self.player_username = player_username
        self.player_uuid = player_uuid
        self.bans = bans
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.frontend_dir = os.path.join(self.script_dir, "SecretFrontend")

    def generate_report(self):
        try:
            ban_report = self._construct_report_dict()
            self._write_report_to_file(ban_report)
            self._serve_report_and_open_browser()
        except Exception as e:
            print(f"An error occurred while generating the report: {e}")

    def _construct_report_dict(self):
        return {
            "username": self.player_username,
            "uuid": self.player_uuid,
            "bans": self.bans,
            "totalbans": len(self.bans),
            "skinurl": "",
            "pastskins": ["", "", ""]
        }

    def _write_report_to_file(self, report_data):
        bans_file = os.path.join(self.frontend_dir, "bans.json")
        with open(bans_file, "w", encoding="utf-8") as bans_json:
            json.dump(report_data, bans_json, indent=4, default=self._to_json)

    def _serve_report_and_open_browser(self):
        os.chdir(self.frontend_dir)
        server_cmd = [sys.executable, "-m", "http.server", "--bind", "127.0.0.1", "8000"]
        with subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p: #nosec
            try:
                webbrowser.open("http://127.0.0.1:8000/index.html", new=2, autoraise=True)
                time.sleep(5)  # Keep the server running for a short time
            finally:
                p.terminate()  # Make sure the server is terminated
                p.wait()  # Wait for the process to terminate

    def _to_json(self, obj):
        return obj.to_json() if hasattr(obj, 'to_json') else None

# Example usage:
# player_report = PlayerReport("player1", "uuid-1234", bans_list)
# player_report.generate_report()