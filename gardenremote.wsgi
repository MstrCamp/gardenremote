#! /usr/bin/python

# import time
import logging
import logging.handlers
import os
import sys


def log_setup(base_path: str):
    log_handler = logging.handlers.RotatingFileHandler(base_path + '/log/app.log', maxBytes=10000000, backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    # formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)


base_path = os.path.dirname(__file__)

log_setup(base_path)
logging.info("Starting application...")
sys.path.insert(0, base_path)
# use packages from the virtualenv instead of global
sys.path.insert(0, base_path + "/venv/lib/python3.9/site-packages")

from app import app as application

application.secret_key = 'anything you wish'

logging.info("Application started.")
