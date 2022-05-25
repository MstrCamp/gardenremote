from __future__ import annotations

import logging
from enum import Enum
from os import environ
from random import choice

if environ.get('SENSORS_UNAVAILABLE') == '1':
    logging.debug("Using Mock Sensors instead of real ones")
    from gpio.mock import *
else:
    from digitalio import DigitalInOut, Direction
    from board import *
    from microcontroller import Pin


class RelayState(Enum):
    ON = False
    OFF = True

    def other(self) -> RelayState:
        return RelayState(not self.value)


class MockRelay:
    def __init__(self, initial_state: bool = None):
        if initial_state is None:
            self.state = choice([True, False])
        else:
            self.state = initial_state

    @property
    def value(self) -> bool:
        return self.state

    @value.setter
    def value(self, value: bool):
        self.state = value


class Relay:
    """Wraps DigitalInOut for convenience"""

    def __init__(self, name: str, pin: Pin = None, initial_state: RelayState = None):
        self.name = name
        if environ.get('SENSORS_UNAVAILABLE') == '1' or pin is None:
            self.io = MockRelay(initial_state)
        else:
            self.io = DigitalInOut(pin)
            self.io.direction = Direction.OUTPUT
            if initial_state is not None:
                self.io.value = initial_state.value

    @property
    def state(self) -> RelayState:
        return RelayState(self.io.value)

    @state.setter
    def state(self, state: RelayState):
        self.io.value = state.value

    def toggle(self) -> RelayState:
        """toggles the state of the relay, returns the new relaystate"""
        self.io.value = not self.io.value
        return self.state

    def serialize(self):
        return {
            "name": self.name,
            "state": self.state.name
        }


relays: dict[str, Relay] = {
    "pool_lights": Relay("Pool Licht", D14),
    "outdoor_lights": Relay("Außenlicht", D15)
}

if __name__ == "__main__":
    from time import sleep

    for r in relays.values():
        r.state = RelayState.OFF

    for i in range(6):
        for key, value in relays.items():
            value.toggle()
            print(f"{key} should be: {value.state}")
        sleep(0.5)
