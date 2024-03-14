import json
import re
import sqlite3
import uuid
from datetime import datetime

import requests
from utils import get_player_username, get_player_uuid
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from rq.job import Job
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import timedelta
from libs.Tokens import verify_base64
from player_report import PlayerReport
from scraper.pipelines import BanPipeline

app = FastAPI()
queue = Queue(connection=Redis())
username_regex = re.compile(r"^[a-zA-Z0-9_]{3,16}$")
uuid_regex = re.compile(
    r"^(?:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}|[0-9a-fA-F]{32})$"
)

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root_route():
    return {"message": "The server is online!"}


class ReportInformation(BaseModel):
    token: str
    player: str


def run_crawler(username, uuid_dash, task_job_id):
    # Initialize the CrawlerRunner
    crawler_runner = CrawlerProcess(get_project_settings())
    # Run the spiders and store the results in the BanPipeline
    blacklisted_sources = ["DemocracycraftSpider"]
    for spider_name in crawler_runner.spider_loader.list():
        if spider_name in blacklisted_sources:
            print(f"Skipping {spider_name} - Blacklisted")
        else:
            if "-" in uuid_dash:
                player_uuid = uuid_dash.replace("-", "")
                player_uuid_dash = uuid_dash
            else:
                player_uuid = uuid_dash
                player_uuid_dash = str(uuid.UUID(uuid_dash))

            # if spider_name == "SyuuSpider":
            crawler_runner.crawl(
                spider_name,
                username=username,
                player_uuid=player_uuid,
                player_uuid_dash=player_uuid_dash,
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
    return redis_key  # Return the Redis key where the results are stored


@app.post("/generate_report")
async def generate_report(input: ReportInformation = Body(...)):
    # Verify information.
    if input.token is None or input.token == "" or verify_base64(input.token) is False:
        return {"success": False, "error": "You have not provided a valid token."}

    player_username = None
    player_uuid = None
    if username_regex.match(input.player):
        _player_uuid = get_player_uuid(input.player)
        if player_uuid is type(dict):
            return player_uuid
        else:
            player_uuid = _player_uuid
            player_username = input.player

    elif uuid_regex.match(input.player):
        _player_username = get_player_username(input.player)
        if player_username is type(dict):
            return player_username
        else:
            player_username = _player_username
            player_uuid = input.player
    else:
        return {
            "success": False,
            "error": "You have not provided a valid username or UUID.",
        }

    # Check if token is valid with database.
    connection = sqlite3.Connection("databases/users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE token = ?", (input.token,))
    rows = cursor.fetchall()
    if len(rows) > 1:
        return {"success": False, "error": "More than one user with same token."}
    if len(rows) == 0:
        return {"success": False, "error": "Token does not exist in our database."}

    # Check if the cached data is less than   1 month old
    one_month_ago = int((datetime.now() - timedelta(days=30)).timestamp())
    cache_connection = sqlite3.Connection("databases/cache.db")
    cache_cursor = cache_connection.cursor()
    user_exist = cache_cursor.execute(
        "SELECT * FROM cache WHERE player_uuid = ?", (player_uuid.replace("-", ""),)
    ).fetchone()

    # Used for testing new sources bypassing the cache
    # user_exist = cache_cursor.execute("SELECT * FROM cache WHERE player_uuid = ?", ("test",)).fetchone()

    if user_exist and user_exist[2] >= one_month_ago:
        # Data is less than 1 month old, return the job_id from the cache
        return {"success": True, "data": user_exist[0]}
    else:
        # Data is older than 1 month, enqueue a new job
        task_job_id = str(uuid.uuid4())
        queue.enqueue(
            run_crawler,
            username=player_username,
            uuid_dash=player_uuid,
            task_job_id=task_job_id,
            job_id=task_job_id,
            result_ttl=600,
        )
        return {"success": True, "data": task_job_id}


@app.post("/check_report/{job_id}")
async def check_report(job_id: str):
    redis_conn = Redis()
    job = Job.fetch(job_id, connection=redis_conn)
    if not job.is_finished:
        return {"success": False, "message": "Results are not available yet."}

    result = job.latest_result()
    if not result.type == result.Type.SUCCESSFUL:
        return {"success": False, "error": "Job was not successful."}

    report_data = json.loads((redis_conn.get(job.return_value()).decode("utf-8")))
    player_report = PlayerReport(
        job.kwargs.get("username"),
        job.kwargs.get("uuid_dash"),
        sorted(report_data, key=lambda x: x["source"]),
    )

    # Serialize the report data to a JSON string
    report_json = json.dumps(player_report.generate_report())

    # Check if the job_id exists in the cache
    cache_connection = sqlite3.Connection("databases/cache.db")
    cache_cursor = cache_connection.cursor()
    cache_cursor.execute("SELECT * FROM cache WHERE job_id = ?", (job_id,))
    job_exists = cache_cursor.fetchone()

    if job_exists:
        # If the job_id exists, return the existing data
        return {"success": True, "data": json.loads(job_exists[1])}
    else:
        # If the job_id does not exist, insert new data
        cache_cursor.execute(
            "INSERT INTO cache (job_id, ban_data, timestamp, player_uuid) VALUES (?, ?, ?, ?)",
            (
                job_id,
                report_json,
                int(datetime.now().timestamp()),
                job.kwargs.get("uuid_dash").replace("-", ""),
            ),
        )
        cache_connection.commit()
        print(f"Job: {job_id} - UUID: {job.kwargs.get('uuid_dash')} added to cache")
        return {"success": True, "data": player_report.generate_report()}
