import os
import platform
import sys

from flask import abort, jsonify
from flask import render_template, Response
from werkzeug.exceptions import HTTPException

from app import app
from gpio.relay import relays, Relay, RelayState
from gpio.sensor import sensors
from sse.MessageAnnouncer import announcer
from sse.util import format_sse


@app.route('/sensor/<device>')
@app.route('/sensor/<device>/<prop>')
def sensor(device: str, prop: str = None):
    if device.lower() == "all":
        return jsonify(sensors=dict([(key, value.serialize()) for key, value in sensors.items()]))
    if device in sensors:
        print("In section single".format(device, str), file=sys.stderr)
        sensor = sensors.get(device)
        if prop is None:
            return jsonify(sensor.serialize())
        if hasattr(sensor, prop):
            return str(getattr(sensors.get(device), prop))
    abort(404)


@app.route('/relay/<device>')
@app.route('/relay/<device>/<function>')
def relay(device: str, function: str = None):
    if device.lower() == "all":
        return jsonify(relays=dict([(key, value.serialize()) for key, value in relays.items()]))
    elif device not in relays:
        abort(404)
    r: Relay = relays.get(device)

    if function is None:
        return jsonify(r.serialize())
    else:
        function = function.lower()
        if function == "toggle":
            r.toggle()
        elif function == "on":
            r.state = RelayState.ON
        elif function == "off":
            r.state = RelayState.OFF
        else:
            abort(404)
        return jsonify(r.serialize())


@app.route('/remote')
def remote():
    functions = ["Aussenlicht",
                 "Finnhuette",
                 "Pool Pumpe",
                 "Pool Licht",
                 "LED Licht",
                 "Party Licht",
                 "Vitrine",
                 "3D Drucker",
                 "Wasserboiler",
                 "Rolladen"]
    return render_template('remote.html', title='Remote', functions=functions)


@app.route('/os')
def route_os():
    return {
        "Name of the operating system:": os.name,
        "Name of the OS system:": platform.system(),
        "Version of the operating system:": platform.release()
    }


@app.route('/ping')
def ping():
    msg = format_sse(data='pong')
    announcer.announce(msg=msg)
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


@app.route('/coffee')
def coffee():
    abort(418)


@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        code = e.code
        return render_template("error.html", code=code, reason=e.name)
    else:
        return render_template("error.html", code=500, reason=str(e))
