import random
from typing import Union


class MockSensor:
    """Mocks the function of the DHT11 Sensor for testing and development purposes."""

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
