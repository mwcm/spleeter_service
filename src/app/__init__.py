# stub
from flask import Flask
from simplekv.fs import FilesystemStore
from flask_kvsession import KVSessionExtension
from config import Config

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
def create_app(config_class=Config):
    app = Flask(__name__)

    app.logger.info(f"using config: {config_class}")

    app.config.from_object(config_class)

    store = FilesystemStore(app.config.get("KV_STORE"))
    KVSessionExtension(store, app)

    # TODO:
    # if dev else deployment

    return app
