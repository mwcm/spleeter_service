# stub
from flask import Flask
from simplekv.fs import FilesystemStore
from flask_kvsession import KVSessionExtension
from config import Config

# ty to https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
app = Flask(__name__)

from app.main import routes

app.logger.info(f"using config: {Config}")

app.config.from_object(Config)

store = FilesystemStore(app.config.get("KV_STORE"))
KVSessionExtension(store, app)

# TODO:
# if dev else deployment
# logging
