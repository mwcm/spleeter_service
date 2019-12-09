import requests
import pafy
from app import app
from youtube_dl import YoutubeDL
import subprocess
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util


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
ydl_opts = {
    "format": "bestaudio/best",
    "extract_audio": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "320",
        }
    ],
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
    "noplaylist": True,
    "max_downloads": 1,
    "default_search": "ytsearch",
}


class YoutubeHelper(object):
    def __init__(self):
        self.ydl = YoutubeDL(ydl_opts)
        return

    def download(self, search):
        results = self.ydl.download(search)
        app.logger.warning(f"DOWNLOAD: {results}")
        return results

    def soup(search):

        query = f"{app.config['YT_SEARCH_URL']}{search.replace(' ', '+')}"

        page = requests.get(query)

        soup = BeautifulSoup(page.content, "html.parser")

        vids = soup.findAll("a", attrs={"class": "yt-uix-tile-link"})

        youtube_list = []

        [youtube_list.append("https://www.youtube.com" + v["href"]) for v in vids[:3]]

        soundcloud_list = []
        main = "https://soundcloud.com/search?q=" + search.replace(" ", "%20")

        page = requests.get(main)
        soup = BeautifulSoup(page.content, "html.parser")

        for link in soup.find_all("a", href=True):
            soundcloud_list.append("https://soundcloud.com" + link["href"])

        soundcloud_list = soundcloud_list[6:9]

        return youtube_list, soundcloud_list

