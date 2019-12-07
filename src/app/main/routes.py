import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, g
from werkzeug.utils import secure_filename
from app import app, store
from app.main.spleeter import spleeter_setup
from app.utils import allowed_extensions


@app.route("/")
@app.route("/index")
def index():
    return "Hello, World!"


@app.route("/go", methods=["GET", "POST"])
def start_aeiou():
    separators, audio_loader = spleeter_setup()
    app.logger.warning("START")
    waveform, rate = audio_loader.load(f'{app.config["SPLEETER_IN"]}test.mp3')
    app.logger.warning("LOADED")
    result = seperators[2].separate(waveform)
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

