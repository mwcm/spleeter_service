from flask import url_for
import requests
from app import app
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        app.logger.warning(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


# add vars?
class YoutubeHelper(object):
    def download(self, search):
        # extension = app.config["YT_EXT"]
        filename = f"{search}".replace(" ", "")  # ".{extension}".replace(" ", "")
        path = f'{app.config["SPLEETER_IN"]}{filename}'
        ydl_opts = {
            "format": "bestaudio/best",
            "extract_audio": True,
            "outtmpl": f"{path}.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": f"{app.config['YT_EXT']}",
                    "preferredquality": "999",
                }
            ],
            "logger": MyLogger(),
            "progress_hooks": [my_hook],
            "noplaylist": True,
            "max_downloads": 1,
            "default_search": "ytsearch",
        }
        ydl = YoutubeDL(ydl_opts)
        ydl.download([search])
        with app.app_context():
            return url_for("uploaded", filename=filename)

    def search(search):

        query = f"{app.config['YT_SEARCH_URL']}{search.replace(' ', '+')}"

        page = requests.get(query)

        soup = BeautifulSoup(page.content, "html.parser")

        vids = soup.findAll("a", attrs={"class": "yt-uix-tile-link"})

        results = []

        # only first result
        [results.append("https://www.youtube.com" + v["href"]) for v in vids[:1]]

        return results

