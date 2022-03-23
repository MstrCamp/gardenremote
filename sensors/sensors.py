import logging
import os
from typing import Callable, Union

from sensors.MockSensor import MockSensor

if os.environ.get('SENSORS_UNAVAILABLE') == '1':
    indoorSensor = MockSensor()
    outdoorSensor = MockSensor()
else:
    import adafruit_dht
    from board import D2, D3
    indoorSensor = adafruit_dht.DHT11(D2)
    outdoorSensor = adafruit_dht.DHT11(D3)


def get_temp_indoor() -> Union[int, float, None]:
    return get_value(lambda: indoorSensor.temperature)


def get_temp_outdoor() -> Union[int, float, None]:
    return get_value(lambda: outdoorSensor.temperature)


def get_humidity_outdoor() -> Union[int, float, None]:
    return get_value(lambda: outdoorSensor.humidity)


def get_value(get: Callable[[], Union[int, float, None]]) -> Union[int, float, None]:
    value: Union[int, float, None] = None
    while True:
        try:
            value = get()
        except RuntimeError as e:
            logging.info("Reading from Sensor failed. Reason: {reason} Retrying...".format(reason=e))
            continue
        break
    return value
