from pathlib import Path


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
        self.frontend_dir = self.script_dir / "report"

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
            print(self.bans)
            return self._construct_report_dict()
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
