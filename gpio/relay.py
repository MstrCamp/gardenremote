from __future__ import annotations

import logging
import threading
import time
from enum import Enum
from os import environ

from sse.MessageAnnouncer import announcer
from sse.util import format_sse, dataToJson, MessageType

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


class ManagementState(Enum):
    MANUAL = False
    AUTO = True

    def other(self) -> ManagementState:
        return ManagementState(not self.value)


class ShutterState(Enum):
    CLOSED = False
    OPEN = True

    def other(self) -> ShutterState:
        return ShutterState(not self.value)


class MockRelay:
    def __init__(self, initial_state: bool = None):
        if initial_state is None:
            self.state = True  # choice([True, False])
        else:
            self.state = initial_state

    @property
    def value(self) -> bool:
        return self.state

    @value.setter
    def value(self, val: bool):
        self.state = val


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

    def on(self):
        self.state = RelayState.ON

    def off(self):
        self.state = RelayState.OFF

    def toggle(self) -> RelayState:
        """toggles the state of the relay, returns the new relaystate"""
        self.io.value = not self.io.value
        return self.state

    def serialize(self):
        return {
            "name": self.name,
            "state": self.state.name
        }


class Button(Relay):
    """ Relay, that toggles back after a second """

    def __init__(self, name: str, pin: Pin = None, initial_state: RelayState = None):
        super(Button, self).__init__(name, pin, initial_state)
        self.lock = threading.Lock()

    def press(self):
        with self.lock:
            self.state = RelayState.ON
            time.sleep(1)
            self.state = RelayState.OFF


class ManagedShutter:
    def __init__(self, name: str, pin_open: Pin = None, pin_close: Pin = None, initial_state: ShutterState = None,
                 management_state: ManagementState = ManagementState.AUTO):
        self.name = name
        self.open_button = Button("open", pin_open, RelayState.OFF)
        self.close_button = Button("close", pin_close, RelayState.OFF)
        if initial_state is not None:
            self._state = initial_state
        else:
            self._state = ShutterState.OPEN
        self.management_state = management_state

    @property
    def state(self) -> ShutterState:
        return self._state

    @state.setter
    def state(self, state: ShutterState):
        self._state = state
        if state == ShutterState.OPEN:
            self.open_button.press()
        else:
            self.close_button.press()

    @property
    def is_open(self) -> bool:
        return self.state.value

    @property
    def is_closed(self) -> bool:
        return not self.state.value

    def toggle_shutter(self):
        self.state = self.state.other()

    def open(self):
        if self.is_closed:
            self.state = ShutterState.OPEN

    def close(self):
        if self.is_open:
            self.state = ShutterState.CLOSED

    def toggle_management_state(self):
        self.management_state = self.management_state.other()

    @property
    def is_managed(self) -> bool:
        return self.management_state.value

    def manual(self):
        self.management_state = ManagementState.MANUAL

    def auto(self):
        self.management_state = ManagementState.AUTO

    def serialize(self):
        return {
            "name": self.name,
            "state": self.state.name,
            "management_state": self.management_state.name
        }


relays: dict[str, Relay] = {
    "relay_pool_lights": Relay("Pool Licht"),
    "relay_outdoor_lights": Relay("Außenlicht"),
    "relay_cabin": Relay("Finnhuette", initial_state=RelayState.ON),
    "relay_pool_pump": Relay("Pool Pumpe"),
    "relay_led_lights": Relay("LED Licht"),
    "relay_party_lights": Relay("Party Licht", initial_state=RelayState.ON),
    "relay_cabinet": Relay("Vitrine", initial_state=RelayState.ON),
    "relay_3dprinter": Relay("3D Drucker"),
    "relay_boiler": Relay("Wasserboiler"),
}


def broadcast_states():
    announcer.announce(
        format_sse(dataToJson(MessageType.RELAY, dict([(key, value.serialize()) for key, value in relays.items()]))))


shutters: dict[str, ManagedShutter] = {
    "shutter_main": ManagedShutter("Rollladen", D14, D15, management_state=ManagementState.AUTO)
}


def broadcast_shutters():
    announcer.announce(
        format_sse(
            dataToJson(MessageType.SHUTTER, dict([(key, value.serialize()) for key, value in shutters.items()]))))


if __name__ == "__main__":
    from time import sleep

    for r in relays.values():
        r.state = RelayState.OFF

    for i in range(6):
        for key, value in relays.items():
            value.toggle()
            print(f"{key} should be: {value.state}")
        sleep(0.5)
