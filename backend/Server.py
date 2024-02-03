from fastapi import FastAPI, Body
from pydantic import BaseModel
from libs.Tokens import verify_base64
import re
import sqlite3

app = FastAPI()

@app.get("/")
def root_route():
    return {
        "message": "The server is online!"
    }

username_regex = re.compile(r"^[a-zA-Z0-9_]{3,16}$")

class ReportInformation(BaseModel):
    token: str
    username: str

@app.get("/generate_report")
def generate_report(input: ReportInformation = Body(...)):
    # Verify information.
    if input.token is None or input.token is "" or verify_base64(input.token) is False:
        return {
            "success": False,
            "error": "You have not provided a valid token."
        }
    if username_regex.match(input.username) is None:
        return {
            "success": False,
            "error": "You have not provided a valid username."
        }
    # Check if token is valid with database.
    connection = sqlite3.Connection("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE token = ?", (input.token))
    rows = cursor.fetchall()
    if len(rows) > 1:
        return {
            "success": False,
            "message": "More than one user with same token."
        }
    if rows == 0:
        return {
            "success": False,
            "message": "Token does not exist in our database."
        }
    # TODO Generate report.
    return {
        "success": True,
        "message": "Not implemented yet."
    }