from fastapi import FastAPI, Body
from pydantic import BaseModel
from libs.Tokens import verify_base64
import re
import sqlite3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.pipelines import BanPipeline
from player_report import PlayerReport
import json
from redis import Redis
import asyncio
from rq import Queue
from rq.job import Job
import uuid

# setup()
app = FastAPI()
queue = Queue(connection=Redis())

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
    
def run_crawler(username, uuid_dash, task_job_id):
    # Initialize the CrawlerRunner
    crawler_runner = CrawlerProcess(get_project_settings())
    # Run the spiders and store the results in the BanPipeline
    for spider_name in crawler_runner.spider_loader.list():
        crawler_runner.crawl(
            spider_name,
            username=username,
            player_uuid=uuid_dash.replace("-", ""),
            player_uuid_dash=uuid_dash,
        )
    # Start the crawling process
    crawler_runner.start()
    # Wait for the crawling to finish
    crawler_runner.join()
    # Get the results from the BanPipeline
    ban_pipeline = BanPipeline()
    results = ban_pipeline.get_bans()
    # Convert each BanItem to a JSON-compatible dictionary
    results_dict = [item.to_json() for item in results]
    # Serialize the results to a JSON string
    serialized_results = json.dumps(results_dict)
    # Save the result to Redis
    redis_conn = Redis()
    redis_key = f"crawler_results:{task_job_id}"
    redis_conn.set(redis_key, serialized_results)
    return redis_key # Return the Redis key where the results are stored

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
    
    # Enqueue the job
    task_job_id = str(uuid.uuid4())
    queue.enqueue(run_crawler, username=input.username, uuid_dash=input.uuid_dash, task_job_id=task_job_id, job_id=task_job_id, result_ttl=600)
    return {"status": "sucessful", "job_id": task_job_id}


@app.get("/check_report/{job_id}")
async def check_report(job_id: str):
    redis_conn = Redis()
    job = Job.fetch(job_id, connection=redis_conn)
    if job.is_finished:
        result = job.latest_result()
        if result.type == result.Type.SUCCESSFUL:
            report_data = json.loads((redis_conn.get(job.return_value()).decode("utf-8")))
            player_report = PlayerReport(
                job.kwargs.get("username"),
                job.kwargs.get("uuid_dash"),
                sorted(report_data, key=lambda x: x["source"]))
            return player_report.generate_report()
        else:
            return {"success": False, "message": "Job was not successful", "result": str(result)}
    else:
        return {"success": False, "message": "Results not available yet"}