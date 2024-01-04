from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/report")
def get_report():
    with open("bans.json", "r") as f:
        report_details = json.load(f)
    return jsonify(report_details)


app.run(debug=False, host="127.0.0.1", port=8000)
