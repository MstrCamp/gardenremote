import logging
import random
from enum import Enum
from os import environ
from typing import Callable, Dict
from typing import Union

from sse.MessageAnnouncer import announcer
from sse.util import format_sse, dataToJson, MessageType

if environ.get('SENSORS_UNAVAILABLE') == '1':
    logging.info("Using Mock Sensors instead of real ones")
    from gpio.mock import *
else:
    from adafruit_dht import *
    from board import *
    from microcontroller import Pin


class MockDHT:
    """Mocks the function of the DHT11 and DHT22 sensors for testing and development purposes."""

    # noinspection PyUnusedLocal
    def __init__(self, pin: Pin = None):
        """Construtor to mimic constructors of real Sensor classes"""
        pass

    @property
    def temperature(self) -> Union[int, float, None]:
        """[MOCK] temperature current reading.  It makes sure a reading is available

        Raises RuntimeError exception for checksum failure and for insufficient
        data returned from the device (try again)
        """
        return random.randrange(-50, 50)

    @property
    def humidity(self) -> Union[int, float, None]:
        """[MOCK] humidity current reading. It makes sure a reading is available

        Raises RuntimeError exception for checksum failure and for insufficient
        data returned from the device (try again)
        """

        return random.randrange(0, 100)

    def exit(self):
        pass


class SensorTypeTemperature(Enum):
    MOCK = MockDHT,
    DHT11 = DHT11,
    DHT21 = DHT21,
    DHT22 = DHT22

    def __init__(self, clazz):
        self.clazz = clazz


class TemperatureSensor:
    """Wraps functionality of DHT11 Sensors to improve reliability of reading values."""
    s: Union[MockDHT, DHTBase]

    def __init__(self, name: str, sensor_type: SensorTypeTemperature = SensorTypeTemperature.MOCK, pin: Pin = None):
        self.name = name
        if environ.get('SENSORS_UNAVAILABLE') == '1' or pin is None:
            self.s = MockDHT()
        else:
            self.s = sensor_type.clazz(pin)

    def __del__(self):
        self.s.exit()

    @property
    def temperature(self) -> Union[int, float, None]:
        """Temperature as int, float or None if reading from sensor failed"""
        return _get_value(lambda: self.s.temperature)

    @property
    def humidity(self) -> Union[int, float, None]:
        """Humidity as int, float or None if reading from sensor failed"""
        return _get_value(lambda: self.s.humidity)

    def serialize(self):
        return {
            "name": self.name,
            "temperature": self.temperature,
            "humidity": self.humidity
        }


class LightState(Enum):
    NIGHT = False
    DAY = True

    @property
    def is_day(self) -> bool:
        return self.value

    @property
    def is_night(self) -> bool:
        return not self.value


class MockDigitalInOut:
    """Mocks the function of a digital input for testing and development purposes"""

    # noinspection PyUnusedLocal
    def __init__(self, pin: Pin = None):
        """Construtor to mimic constructors of real Sensor classes"""
        pass

    @property
    def value(self) -> bool:
        return random.choice([True, False])


class SensorTypeLight(Enum):
    MOCK = MockDigitalInOut,
    REAL = DigitalInOut

    def __init__(self, clazz):
        self.clazz = clazz


class LightSensor:
    """Wraps functionality of light sensors to improve reliability of reading values."""
    s: Union[DigitalInOut, MockDigitalInOut]

    def __init__(self, name: str, sensor_type: SensorTypeLight = SensorTypeLight.MOCK, pin: Pin = None):
        self.name = name
        if environ.get('SENSORS_UNAVAILABLE') == '1' or pin is None:
            self.s = MockDigitalInOut()
        else:
            self.s = sensor_type.clazz(pin)

    @property
    def state(self) -> LightState:
        return LightState(self.s.value)


def _get_value(get: Callable[[], Union[int, float, None]], max_retry: int = 20) -> Union[int, float, None]:
    """tries to read value from sensor until it succeeds. If no max retry value is given tries for a maximum of 10
    times """
    if max_retry <= 0:
        raise ValueError('Negative values not allowed!')
    value: Union[int, float, None] = None
    while True:
        try:
            value = get()
            if value is None:
                raise RuntimeError
        except RuntimeError as e:
            logging.info(f"Reading from Sensor failed. Reason: {e} Retrying...")
            max_retry -= 1
            if max_retry > 0:
                continue
        break
    return value


temp_sensors: Dict[str, TemperatureSensor] = {
    "sensor_indoor": TemperatureSensor("Innen", SensorTypeTemperature.DHT22, D2),
    # "indoor": Sensor("Innen", SensorType.MOCK),
    "sensor_outdoor": TemperatureSensor("Außen", SensorTypeTemperature.DHT22, D3)
}

light_sensors: Dict[str, LightSensor] = {
    "light_outdoor": LightSensor("Außenlicht", sensor_type=SensorTypeLight.REAL, pin=D26)
}


def broadcast_data():
    announcer.announce(
        format_sse(
            dataToJson(MessageType.SENSOR, dict([(key, value.serialize()) for key, value in temp_sensors.items()]))))


if __name__ == "__main__":
    sensor = temp_sensors.get("sensor_indoor")
    print(f"Temp: {sensor.temperature}°C")
    print(f"Hum:  {sensor.humidity}%")

    sensor = light_sensors.get("light_outdoor")
    print(f"Light:  {sensor.state}")
