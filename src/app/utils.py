import os
from uuid import uuid4
from app import app
from youtube_dl import YoutubeDL

# TODO: maybe add vars?

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
}
from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


def ydl_helper(song):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=BaW_jenozKc"])


def allowed_extensions(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def generate_random_filename(upload_directory, extension):
    filename = str(uuid4())
    filename = os.path.join(upload_directory, filename + "." + extension)
    return filename
