from fastapi import FastAPI, Body
from pydantic import BaseModel
from libs.Tokens import verify_base64
import re

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
    # TODO Generate report.
    return {
        "success": True,
        "message": "Not implemented yet."
    }