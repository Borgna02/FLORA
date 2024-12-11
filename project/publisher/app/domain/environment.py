import random
from domain.season import Season
from domain.geographical_area import GeographicalArea
from domain.weather import Weather
from lib.utils import *

ITALY_TEMPERATURE_BY_SEASON = {
    Season.WINTER: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 0.0,
            MAX_THRESHOLD_KEY: 5.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 5.0,
            MAX_THRESHOLD_KEY: 10.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 10.0,
            MAX_THRESHOLD_KEY: 15.0
        }
    },
    Season.SPRING: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 5.0,
            MAX_THRESHOLD_KEY: 15.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 10.0,
            MAX_THRESHOLD_KEY: 20.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 15.0,
            MAX_THRESHOLD_KEY: 25.0
        }
    },
    Season.SUMMER: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 15.0,
            MAX_THRESHOLD_KEY: 25.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 20.0,
            MAX_THRESHOLD_KEY: 30.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 25.0,
            MAX_THRESHOLD_KEY: 35.0
        }
    },
    Season.AUTUMN: {
        GeographicalArea.NORTH: {
            MIN_THRESHOLD_KEY: 5.0,
            MAX_THRESHOLD_KEY: 15.0
        },
        GeographicalArea.CENTER: {
            MIN_THRESHOLD_KEY: 10.0,
            MAX_THRESHOLD_KEY: 20.0
        },
        GeographicalArea.SOUTH: {
            MIN_THRESHOLD_KEY: 15.0,
            MAX_THRESHOLD_KEY: 25.0
        }
    }
}

TEMPERATURE_FACTOR_WHEN_RAINING = {
    MIN_THRESHOLD_KEY: -5.0,
    MAX_THRESHOLD_KEY: -3.0
}

TEMPERATURE_FACTOR_WHEN_SNOWING = {
    MIN_THRESHOLD_KEY: -10.0,
    MAX_THRESHOLD_KEY: -8.0
}


def compute_temperature_factor(min_threshold, max_threshold):
    return random.uniform(min_threshold, max_threshold)


def compute_temperature_factor_when_raining():
    return compute_temperature_factor(TEMPERATURE_FACTOR_WHEN_RAINING[MIN_THRESHOLD_KEY],
                                      TEMPERATURE_FACTOR_WHEN_RAINING[MAX_THRESHOLD_KEY])


def compute_temperature_factor_when_snowing():
    return compute_temperature_factor(TEMPERATURE_FACTOR_WHEN_SNOWING[MIN_THRESHOLD_KEY],
                                      TEMPERATURE_FACTOR_WHEN_SNOWING[MAX_THRESHOLD_KEY])


class Environment:

    def __init__(self, geographical_area=None, current_season=None, is_raining=False, is_snowing=False):
        if geographical_area is None:
            match random.randint(1, 3):
                case 1:
                    self.__geographical_area = GeographicalArea.NORTH
                case 2:
                    self.__geographical_area = GeographicalArea.CENTER
                case 3:
                    self.__geographical_area = GeographicalArea.SOUTH
        else:
            self.__geographical_area = geographical_area

        if current_season is None:
            match random.randint(1, 4):
                case 1:
                    current_season = Season.SPRING
                case 2:
                    current_season = Season.SUMMER
                case 3:
                    current_season = Season.AUTUMN
                case 4:
                    current_season = Season.WINTER

        self.__current_temperature = random.uniform(
            ITALY_TEMPERATURE_BY_SEASON[current_season][self.__geographical_area][MIN_THRESHOLD_KEY],
            ITALY_TEMPERATURE_BY_SEASON[current_season][self.__geographical_area][MAX_THRESHOLD_KEY])

        self.__weather = Weather(self, current_season, is_raining, is_snowing)

    @property
    def geographical_area(self):
        return self.__geographical_area

    @property
    def current_temperature(self):
        return self.__current_temperature

    @property
    def current_season(self):
        return self.__weather.current_season

    @property
    def is_raining(self):
        return self.__weather.is_raining

    @property
    def is_snowing(self):
        return self.__weather.is_snowing

    def update(self):
        self.__weather.update()
        self.compute_temperature()

    def compute_temperature(self):
        temp_temperature = random.uniform(
            ITALY_TEMPERATURE_BY_SEASON[self.__weather.current_season][self.__geographical_area][MIN_THRESHOLD_KEY],
            ITALY_TEMPERATURE_BY_SEASON[self.__weather.current_season][self.__geographical_area][MAX_THRESHOLD_KEY])

        if self.__weather.is_raining:
            temp_temperature += compute_temperature_factor_when_raining()

        if self.__weather.is_snowing:
            temp_temperature += compute_temperature_factor_when_snowing()

        self.__current_temperature = temp_temperature

    def to_string(self):
        return (f"Environment: "
                f"\n- Geographical Area: {self.__geographical_area}"
                f"\n- Temperature: {self.__current_temperature}"
                f"\n{self.__weather.to_string()}")
