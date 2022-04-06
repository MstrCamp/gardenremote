from flask import Flask
from config import Config
# noinspection PyUnresolvedReferences
from gpio import sensor, relay  # this will ensure initialization of devices

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)

from app import routes
