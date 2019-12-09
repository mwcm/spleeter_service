import os
from flask import Flask
from config import Config

app = Flask(__name__)
app.secret_key = "super_secret"

from app.main import routes

app.config.from_object(Config)
app.logger.warning(f"app configc: {app.config}")
