# stub
from flask import Flask
from simplekv.fs import FilesystemStore
from flask_kvsession import KVSessionExtension

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
def create_app(config_class=Config):
    app = Flask(__name__)

    app.logger.info(f"using config: {config_class}")

    app.config.from_object(config_class)

    store = FilesystemStore("./data")
    KVSessionExtension(store, app)

