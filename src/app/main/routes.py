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
from app.main.seperator import SimpleSeparator
from werkzeug.utils import secure_filename
from app import app
from app.utils import allowed_extensions
from rq import Queue, Connection
from app.main.youtube import YoutubeHelper
from app.main.soundclound import SoundCloudHelper

ythelper = YoutubeHelper()


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


# TODO:
#       route for youtube
#       route for soundcloud
#       route for spotify
#       route for soulseek https://github.com/MehdiBela/soulseek_downloader

# TODO: to decide...
#       option to automatically store w/ google drive or something?
#       should copy to laptop/cloud
#       or access as a volume?


def separate_helper(filename, n):
    allowed_n = ["2", "4", "5"]
    if n not in allowed_n:
        n = "2"
    separator = SimpleSeparator(f"spleeter:{n}stems")
    with Connection(redis.from_url(app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(
            separator.separate_to_file,
            f'{app.config["SPLEETER_IN"]}{filename}',
            destination=f'{app.config["SPLEETER_OUT"]}',
            filename_format="{instrument}.{codec}",
        )
    response_object = {"status": "success", "data": {"task_id": task.get_id()}}
    return response_object


@app.route("/separate/<filename>", methods=["GET"])
def separate(filename):
    n = request.args.get("n")
    response = separate_helper(filename, n)
    return jsonify(response), 202


@app.route("/uploaded/<filename>")
def uploaded(filename):
    return send_from_directory(app.config["SPLEETER_IN"], filename)


@app.route("/separated/<filename>")
def separated(filename):
    return send_from_directory(app.config["SPLEETER_OUT"], filename)


@app.route("/youtube", methods=["GET"])
def youtube():
    song = request.args.get("s")
    file = ythelper.download(song)
    return str(file)


@app.route("/upload", methods=["POST"])
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
            return redirect(url_for("uploaded", filename))


@app.route("/upload_and_separate", methods=["POST"])
def upload_and_separate():
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
                n = request.form.get("n")
                response = separate_helper(filename, n)
            else:
                allowed_extensions
                flash(
                    f"invalid file extension, valid extensions are: {app.config['ALLOWED_EXTENSIONS']}"
                )

            return jsonify(response), 202


# ty https://github.com/gbroccolo/flask-redis-docker/blob/master/webapp/app/main.py
@app.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(app.config["REDIS_URL"])):
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

