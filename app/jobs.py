from gpio.relay import broadcast_states, shutters, ShutterState
from gpio.sensor import broadcast_data, light_sensors, LightState, temp_sensors
from . import scheduler


@scheduler.task('interval', id='do_job_broadcast_sensor_data', minutes=5, misfire_grace_time=900)
def broadcast_sensor_data():
    broadcast_data()


@scheduler.task('interval', id='do_job_broadcast_relay_states', minutes=5, misfire_grace_time=900)
def broadcast_relay_states():
    broadcast_states()


@scheduler.task('cron', id='do_job_morning_shutter', hour='5-9', minute='0,5,10,15,20,25,30,35,40,45,50,55', misfire_grace_time=900)
def morning_shutter():
    light = light_sensors.get("light_outdoor").state
    temp = temp_sensors.get("sensor_outdoor").temperature
    shutter = shutters.get("shutter_main")
    if shutter.is_managed and shutter.is_closed and light.is_day and temp >= 4:
        shutter.open()


@scheduler.task('cron', id='do_job_evening_shutter', hour='15-21', minute='0,5,10,15,20,25,30,35,40,45,50,55', misfire_grace_time=900)
def evening_shutter():
    light = light_sensors.get("light_outdoor").state
    shutter = shutters.get("shutter_main")
    if shutter.is_managed and shutter.is_open and light.is_night:
        shutter.open()
