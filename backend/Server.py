from fastapi import FastAPI, Body
from pydantic import BaseModel
from libs.Tokens import verify_base64
import re
import sqlite3
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scraper.pipelines import BanPipeline
from player_report import PlayerReport
from crochet import setup, run_in_reactor


setup()
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
    uuid_dash: str
    
crawler_runner = CrawlerRunner(get_project_settings())  # Initialize the CrawlerRunner

@run_in_reactor
def run_crawler(input):
    for spider_name in crawler_runner.spider_loader.list():
        crawler_runner.crawl(
            spider_name,
            username=input.username,
            player_uuid=input.uuid_dash.replace("-", ""),
            player_uuid_dash=input.uuid_dash,
        )
    return crawler_runner.join()  # Return the deferred from join, which fires when all crawls are done


@app.get("/generate_report")
async def generate_report(input: ReportInformation = Body(...)):
    # Verify information.
    if input.token is None or input.token == "" or verify_base64(input.token) is False:
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
    cursor.execute("SELECT * FROM users WHERE token = ?", (input.token, ))
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
    
    #TODO FIX | Currently can run once but any runs afterwards will have combined ban lists
    run_crawler(input).wait(timeout=None)
    
    player_report = PlayerReport(
        input.username,
        input.uuid_dash,
        sorted(BanPipeline.bans, key=lambda x: x["source"]),
    )
    return player_report.generate_report()
