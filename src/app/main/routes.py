import os
import redis
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    current_app,
    session,
    jsonify,
)
from werkzeug.utils import secure_filename
from app import app
from app.utils import allowed_extensions

from app.main.seperator import BasicSeparator

from rq import Queue, Connection

REDIS_URL = "redis://redis:6379/0"
REDIS_QUEUES = ["default"]


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


# TODO:
#       make a route to upload AND process the uploaded file
#       route for youtube
#       route for soundcloud
#       route for spotify
#       route for soulseek https://github.com/MehdiBela/soulseek_downloader

# TODO: to decide...
#       option to automatically store w/ google drive or something?
#       should copy to laptop/cloud
#       or access as a volume?


@app.route("/separate_file/<filename>", methods=["GET"])
def separate_file(filename):
    allowed_n = ["2", "4", "5"]
    n = request.args.get("n")
    if n not in allowed_n:
        n = "2"
    separator = BasicSeparator(f"spleeter:{n}stems")
    with Connection(redis.from_url(REDIS_URL)):
        q = Queue()
        task = q.enqueue(
            separator.separate_to_file,
            f'{app.config["SPLEETER_IN"]}{filename}',
            destination=f'{app.config["SPLEETER_OUT"]}',
            filename_format="{instrument}.{codec}",
        )
        response_object = {"status": "success", "data": {"task_id": task.get_id()}}
    return jsonify(response_object), 202


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["SPLEETER_IN"], filename)


@app.route("/complete/<filename>")
def processed_file(filename):
    return send_from_directory(app.config["SPLEETER_OUT"], filename)


@app.route("/upload_file", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if len(request.files) == 0:
            flash("No file")
            return redirect(request.url)

        for file in request.files:
            a_file = request.files[file]

            if a_file.filename == "":
                flash("no file selected")

            if a_file and allowed_extensions(a_file.filename):
                filename = secure_filename(a_file.filename)
                a_file.save(os.path.join(app.config["SPLEETER_IN"], filename))
                return "OK"


# ty https://github.com/gbroccolo/flask-redis-docker/blob/master/webapp/app/main.py
@app.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(REDIS_URL)):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }

        if task.is_failed:
            response_object = {
                "status": "failed",
                "data": {
                    "task_id": task.get_id(),
                    "message": task.exc_info.strip().split("\n")[-1],
                },
            }
    else:
        response_object = {"status": "ERROR: Unable to fetch the task from RQ"}
    return jsonify(response_object)

