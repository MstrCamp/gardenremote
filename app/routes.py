import sys

from flask import abort, jsonify
from flask import render_template, Response
from werkzeug.exceptions import HTTPException

from app import app
from gpio.relay import relays, shutters, Relay, broadcast_states, ManagedShutter, \
    broadcast_shutters
from gpio.sensor import temp_sensors
from sse.MessageAnnouncer import announcer


@app.route('/sensor/<device>')
@app.route('/sensor/<device>/<prop>')
def sensor(device: str, prop: str = None):
    if device.lower() == "all":
        return jsonify(sensors=dict([(key, value.serialize()) for key, value in temp_sensors.items()]))
    if device in temp_sensors:
        print("In section single".format(device, str), file=sys.stderr)
        s = temp_sensors.get(device)
        if prop is None:
            return jsonify(s.serialize())
        if hasattr(s, prop):
            return str(getattr(temp_sensors.get(device), prop))
    abort(404)


@app.route('/relay/<device>')
@app.route('/relay/<device>/<function>')
def relay(device: str, function: str = None):
    if device.lower() == "all":
        return jsonify(relays=dict([(key, value.serialize()) for key, value in relays.items()]))
    elif device not in relays:
        abort(404)
    r: Relay = relays.get(device)

    if function is not None:
        function = function.lower()
        if function == "toggle":
            r.toggle()
        elif function == "on":
            r.on()
        elif function == "off":
            r.off()
        else:
            abort(404)
        broadcast_states()

    return jsonify(r.serialize())


@app.route('/shutter/<device>')
@app.route('/shutter/<device>/<function>')
def shutter(device: str, function: str = None):
    if device.lower() == "all":
        return jsonify(shutters=dict([(key, value.serialize()) for key, value in shutters.items()]))
    elif device not in shutters:
        abort(404)
    s: ManagedShutter = shutters.get(device)
    if function is not None:
        function = function.lower()
        if function == "toggle":
            s.toggle_shutter()
        elif function == "open":
            s.open()
        elif function == "close":
            s.close()
        elif function == "toggle_management":
            s.toggle_management_state()
        elif function == "auto":
            s.auto()
        elif function == "manual":
            s.manual()
        else:
            abort(404)
        broadcast_shutters()

    return jsonify(s.serialize())


@app.route('/remote')
def remote():
    return render_template('remote.html', title='Remote', sensors=temp_sensors, relays=relays, shutters=shutters)


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
