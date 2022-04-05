#! /usr/bin/python

import logging
import sys
# logging.basicConfig(filename="/home/pi/GardenRemote/gardenremote.log")
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/GardenRemote/')

from app import app as application
application.secret_key = 'anything you wish'