import logging
import sys

from flask import Flask
from flask_apscheduler import APScheduler

from config import Config
# noinspection PyUnresolvedReferences
from gpio import sensor, relay  # this will ensure initialization of devices


def log_setup():
    log_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s: %(message)s',
        '%b %d %H:%M:%S')
    # formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)


log_setup()
app = Flask(__name__, static_url_path='')
app.config.from_object(Config)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


from app import routes
from app import jobs
