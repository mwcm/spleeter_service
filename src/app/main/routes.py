import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    current_app,
    session,
)
from werkzeug.utils import secure_filename
from app import app
from app.utils import allowed_extensions

from spleeter.audio.adapter import get_default_audio_adapter
from spleeter.separator import Separator

# ABOVE WORKED IN python3 repl in containe>>>
# separator.separate_to_file('/service/spleeter/in/test.mp3', destination='/service/spleeter/out/', filename_format='{instrument}.{codec}')


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/go", methods=["GET", "POST"])
def start_aeiou():
    app.logger.warning("START")
    ## TODO: why can't instantiate separator here?
    separator = Separator("spleeter:2stems")
    app.logger.warning("LOADED")

    result = separator.separate_to_file(
        f'{app.config["SPLEETER_IN"]}test.mp3',
        destination=f'{app.config["SPLEETER_OUT"]}',
        filename_format="{instrument}.{codec}",
    )
    app.logger.warning("SEPERATED")
    return "OK"


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["SPLEETER_IN"], filename)


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
