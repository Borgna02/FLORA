from sensors.sensor import Sensor
from domain.season import Season
import random
from domain.geographical_area import GeographicalArea
from lib.utils import *

HUMIDITY_PERCENTAGE_BY_SEASON = {
    Season.WINTER: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 75.0,
            MAX_THRESHOLD_KEY: 90.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 70.0,
            MAX_THRESHOLD_KEY: 85.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 65.0,
            MAX_THRESHOLD_KEY: 80.0
        }
    },
    Season.SPRING: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 60.0,
            MAX_THRESHOLD_KEY: 80.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 55.0,
            MAX_THRESHOLD_KEY: 75.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 50.0,
            MAX_THRESHOLD_KEY: 70.0
        }
    },
    Season.SUMMER: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 50.0,
            MAX_THRESHOLD_KEY: 70.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 40.0,
            MAX_THRESHOLD_KEY: 60.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 40.0,
            MAX_THRESHOLD_KEY: 60.0
        }
    },
    Season.AUTUMN: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 70.0,
            MAX_THRESHOLD_KEY: 85.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 65.0,
            MAX_THRESHOLD_KEY: 80.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 60.0,
            MAX_THRESHOLD_KEY: 75.0
        }
    }
}


class HumiditySensor(Sensor):

    def __init__(self, environment):
        super().__init__(environment)

    def read(self):
        if self.environment.is_raining:
            return 100 - random.uniform(0.0, 5.0)

        if self.environment.is_snowing:
            return 80 + random.uniform(0.0, 20.0)

        geographical_area = self.environment.geographical_area
        current_season = self.environment.current_season
        current_temperature = self.environment.current_temperature

        humidity_reading = random.uniform(
            HUMIDITY_PERCENTAGE_BY_SEASON[current_season][geographical_area][MIN_THRESHOLD_KEY],
            HUMIDITY_PERCENTAGE_BY_SEASON[current_season][geographical_area][MAX_THRESHOLD_KEY])
        humidity_reading += (current_temperature * 0.2)  # add noise given by temperature value
        return humidity_reading
