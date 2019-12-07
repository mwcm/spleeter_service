# stub
import os
from flask import Flask
from simplekv.fs import FilesystemStore
from flask_kvsession import KVSessionExtension
from config import Config

# ty to https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
store = FilesystemStore('/service/spleeter/app_data')
app = Flask(__name__)

KVSessionExtension(store, app)

from app.main import routes

app.secret_key = "super_secret"
app.config.from_object(Config)
app.logger.warning(f"using config: {app.config}")

config_paths = [
    app.config["SPLEETER_IN"],
    app.config["SPLEETER_OUT"],
    app.config["KV_STORE"],
]

for p in config_paths:
    if not os.path.exists(p):
        os.makedirs(p)
