from __future__ import unicode_literals
from youtube_dl import YoutubeDL
import subprocess


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


# add vars?
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


class YoutubeHelper(object):
    def __init__(self):
        self.ydl = YoutubeDL(ydl_opts)
        return

    def search(self, text):
        cmd = ["youtube-dl", f'ytsearch:"{text}" -g']
        url_results = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        ).stdout.split()[0]
        return url_results

    def searchfirst(self, text):
        url_results = self.search(text)[0]
        return url_results

    def download(self, url):
        return

