from gpio.relay import relays
from gpio.sensor import sensors
from sse.MessageAnnouncer import announcer
from sse.util import format_sse, MessageType, dataToJson
from . import scheduler

i: int = 0


"""@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def job1():
    global i
    # announcer.announce(format_sse(f"test {i} from interval job"))
    i += 1
"""


@scheduler.task('interval', id='do_job_broadcast_sensor_data', minutes=5, misfire_grace_time=900)
def broadcast_sensor_data():
    announcer.announce(format_sse(dataToJson(MessageType.SENSOR, dict([(key, value.serialize()) for key, value in sensors.items()]))))
