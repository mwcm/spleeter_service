import os


class Config(object):
    DEBUG = os.environ.get("DEBUG", True)
    SPLEETER_IN = os.environ.get("SPLEETER_IN", "/service/spleeter/in/")
    SPLEETER_OUT = os.environ.get("SPLEETER_OUT", "/service/spleeter/out/")
    PORT = os.environ.get("PORT", 6000)
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS", ["mp3", "flac", "wav"])
    SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:6000")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    REDIS_QUEUES = os.environ.get("REDIS_QUEUES", ["default"])
    YT_SEARCH_URL = os.environ.get(
        "YT_SEARCH_URL", "https://www.youtube.com/results?search_query="
    )
    SC_SEARCH_URL = os.environ.get("SC_SEARCH_URL", "https://soundcloud.com/search?q=")


class DeployConfig(Config):
    DEBUG = os.environ.get("DEBUG", False)
    SPLEETER_IN = os.environ.get("SPLEETER_IN", "/service/spleeter/in/")
    SPLEETER_OUT = os.environ.get("SPLEETER_OUT", "/service/spleeter/out/")
    PORT = os.environ.get("PORT", 6000)
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS", ["mp3", "flac", "wav"])
    SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:6000")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    REDIS_QUEUES = os.environ.get("REDIS_QUEUES", ["default"])
    YT_SEARCH_URL = os.environ.get(
        "YT_SEARCH_URL", "https://www.youtube.com/results?search_query="
    )
    SC_SEARCH_URL = os.environ.get("SC_SEARCH_URL", "https://soundcloud.com/search?q=")
