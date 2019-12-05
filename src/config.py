import os


class Config(object):
    DEBUG = os.environ.get("DEBUG", True)
    SPLEETER_IN = os.environ.get("SPLEETER_IN", "/spleeter/in/")
    SPLEETER_OUT = os.environ.get("SPLEETER_OUT", "/spleeter/out/")
    SPLEETER_MODELS = os.environ.get("SPLEETER_MODELS", "/spleeter/models/")
    KV_STORE = os.environ.get("KV_STORE", "/app/data/")


class DeployConfig(Config):
    DEBUG = os.environ.get("DEBUG", False)
    SPLEETER_IN = os.environ.get("SPLEETER_IN", "/spleeter/in/")
    SPLEETER_OUT = os.environ.get("SPLEETER_OUT", "/spleeter/out/")
    SPLEETER_MODELS = os.environ.get("SPLEETER_MODELS", "/spleeter/models/")
    KV_STORE = os.environ.get("KV_STORE", "/app/data/")
