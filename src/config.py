import os


class Config(object):
    DEBUG = os.environ.get("DEBUG", True)
    SPLEETER_IN = os.environ.get("SPLEETER_IN", "/service/spleeter/in/")
    SPLEETER_OUT = os.environ.get("SPLEETER_OUT", "/service/spleeter/out/")
    KV_STORE = os.environ.get("KV_STORE", "/service/spleeter/app_data/")
    PORT = os.environ.get("PORT", 6000)
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS", ["mp3", "flac", "wav"])
    SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:6000")


class DeployConfig(Config):
    DEBUG = os.environ.get("DEBUG", False)
    SPLEETER_IN = os.environ.get("SPLEETER_IN", "/service/spleeter/in/")
    SPLEETER_OUT = os.environ.get("SPLEETER_OUT", "/service/spleeter/out/")
    KV_STORE = os.environ.get("KV_STORE", "/service/spleeter/app_data/")
    PORT = os.environ.get("PORT", 6000)
    ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS", ["mp3", "flac", "wav"])
    SERVER_NAME = os.environ.get("SERVER_NAME", "localhost:6000")
