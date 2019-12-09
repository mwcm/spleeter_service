from flask import url_for
from app import app
from youtube_dl import YoutubeDL


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
    def download(self, search, return_filename=False):
        filename = f"{search}".replace(" ", "")
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
        if return_filename:
            return f"{filename}.{app.config['YT_EXT']}"
        else:
            with app.app_context():
                return url_for("uploaded", filename=filename)
