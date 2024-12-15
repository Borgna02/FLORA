from sensors.sensor import Sensor
from domain.season import Season
import random
from domain.geographical_area import GeographicalArea
from lib.utils import *

PH_RANGE = {
    MIN_THRESHOLD_KEY: 0.0,
    MAX_THRESHOLD_KEY: 14.0
}

PH_LEVEL_BY_SEASON = {
    Season.WINTER: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 0.0,
            MAX_THRESHOLD_KEY: 7.5
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 3.0,
            MAX_THRESHOLD_KEY: 6.5
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 4.0,
            MAX_THRESHOLD_KEY: 7.5
        }
    },
    Season.SPRING: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 4.5,
            MAX_THRESHOLD_KEY: 7.5
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 5.0,
            MAX_THRESHOLD_KEY: 7.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 5.5,
            MAX_THRESHOLD_KEY: 7.0
        }
    },
    Season.SUMMER: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 8.0,
            MAX_THRESHOLD_KEY: 12.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 8.5,
            MAX_THRESHOLD_KEY: 10.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 10.50,
            MAX_THRESHOLD_KEY: 12.0
        }
    },
    Season.AUTUMN: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 9.5,
            MAX_THRESHOLD_KEY: 14.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 9.0,
            MAX_THRESHOLD_KEY: 12.5
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 11.0,
            MAX_THRESHOLD_KEY: 14.0
        }
    }
}


class PHSensor(Sensor):

    def __init__(self, environment):
        super().__init__(environment)

    def read(self):
        geographical_area = self.environment.geographical_area
        current_season = self.environment.current_season
        current_temperature = self.environment.current_temperature
        ph_reading = random.uniform(PH_LEVEL_BY_SEASON[current_season][geographical_area][MIN_THRESHOLD_KEY], PH_LEVEL_BY_SEASON[current_season][geographical_area][MAX_THRESHOLD_KEY])
        ph_reading += (current_temperature * 0.2)  # add noise given by temperature value
        return min(PH_RANGE[MAX_THRESHOLD_KEY], ph_reading)
