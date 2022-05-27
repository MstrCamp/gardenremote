from gpio.relay import broadcast_states
from gpio.sensor import broadcast_data
from . import scheduler


@scheduler.task('interval', id='do_job_broadcast_sensor_data', minutes=5, misfire_grace_time=900)
def broadcast_sensor_data():
    broadcast_data()


@scheduler.task('interval', id='do_job_broadcast_relay_states', minutes=5, misfire_grace_time=900)
def broadcast_relay_states():
    broadcast_states()


@scheduler.task('interval', id='do_job_manage_shutter', minutes=5, misfire_grace_time=900)
def manage_shutter():
    pass
