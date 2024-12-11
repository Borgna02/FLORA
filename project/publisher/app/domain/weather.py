import random
import time
from domain.season import Season
from lib.utils import *

SEASON_CHANGE_INTERVAL_IN_SECONDS = 300  # every 300 seconds (5 minutes) the season must change

RAIN_TIME_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 3,
    MAX_THRESHOLD_KEY: 5
}

SNOW_TIME_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 5,
    MAX_THRESHOLD_KEY: 10
}

WAIT_TIME_UNTIL_NEXT_RAIN_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 60,
    MAX_THRESHOLD_KEY: 120
}

WAIT_TIME_UNTIL_NEXT_SNOW_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 180,
    MAX_THRESHOLD_KEY: 240
}


def compute_snow_time():
    return random.uniform(SNOW_TIME_IN_SECONDS[MIN_THRESHOLD_KEY], SNOW_TIME_IN_SECONDS[MAX_THRESHOLD_KEY])


def compute_rain_time():
    return random.uniform(RAIN_TIME_IN_SECONDS[MIN_THRESHOLD_KEY], RAIN_TIME_IN_SECONDS[MAX_THRESHOLD_KEY])


def compute_wait_time_until_next_rain():
    return random.uniform(WAIT_TIME_UNTIL_NEXT_RAIN_IN_SECONDS[MIN_THRESHOLD_KEY],
                          WAIT_TIME_UNTIL_NEXT_RAIN_IN_SECONDS[MAX_THRESHOLD_KEY])


def compute_wait_time_until_next_snow():
    return random.uniform(WAIT_TIME_UNTIL_NEXT_SNOW_IN_SECONDS[MIN_THRESHOLD_KEY],
                          WAIT_TIME_UNTIL_NEXT_SNOW_IN_SECONDS[MAX_THRESHOLD_KEY])


class Weather:

    def __init__(self, environment, current_season, is_raining=False, is_snowing=False):
        self.__environment = environment
        self.__current_season = current_season
        self.__last_season_changed_time = time.time()

        self.__is_raining = is_raining
        if self.__is_raining:
            self.__rain_time = compute_rain_time()
            self.__rain_start_time = self.__last_season_changed_time
        else:
            self.__rain_time = None
            self.__rain_start_time = None
        self.__wait_time_until_next_rain = None
        self.__last_rain_end_time = None

        self.__is_snowing = False if self.__environment.current_temperature <= 0.0 and (
                is_raining and is_snowing) else is_snowing  # can only snow if temperature is below 0 and can only rain or snow at a time, not both
        if self.__is_snowing:
            self.__snow_time = compute_snow_time()
            self.__snow_start_time = self.__last_season_changed_time
        else:
            self.__snow_time = None
            self.__snow_start_time = None
        self.__wait_time_until_next_snow = None
        self.__last_snow_end_time = None

    @property
    def current_season(self):
        return self.__current_season

    @property
    def is_raining(self):
        return self.__is_raining

    @property
    def is_snowing(self):
        return self.__is_snowing

    def check_if_season_must_be_changed(self):
        time_difference = time.time() - self.__last_season_changed_time
        return time_difference > SEASON_CHANGE_INTERVAL_IN_SECONDS

    def change_season(self):
        match self.__current_season:
            case Season.WINTER:
                return Season.SPRING
            case Season.SPRING:
                return Season.SUMMER
            case Season.SUMMER:
                return Season.AUTUMN
            case Season.AUTUMN:
                return Season.WINTER

    def update(self):
        current_time = time.time()

        if self.check_if_season_must_be_changed():
            self.__current_season = self.change_season()
            self.__last_season_changed_time = current_time

        if self.__is_raining:
            if (current_time - self.__rain_start_time) > self.__rain_time:
                self.__is_raining = False
                self.__rain_time = None
                self.__rain_start_time = None
                self.__last_rain_end_time = time.time()
                self.__wait_time_until_next_rain = compute_wait_time_until_next_rain()
        else:
            if ((not self.__is_snowing) and  # must not be snowing
                    ((self.__last_rain_end_time is None) or ((self.__last_rain_end_time is not None) and (
                            current_time - self.__last_rain_end_time > self.__wait_time_until_next_rain))) and
                    random.randint(0, 100) <= 20):  # 20% of rain
                self.__is_raining = True
                self.__rain_time = compute_rain_time()
                self.__rain_start_time = time.time()
                self.__last_rain_end_time = None
                self.__wait_time_until_next_rain = None

        if self.__is_snowing:
            if (current_time - self.__snow_start_time) > self.__snow_time:
                self.__is_snowing = False
                self.__rain_time = None
                self.__rain_start_time = None
                self.__last_snow_end_time = time.time()
                self.__wait_time_until_next_snow = compute_wait_time_until_next_snow()
        else:
            if ((not self.__is_raining) and  # must not be raining
                    self.__environment.current_temperature <= 0.0 and  # can only snow if temperature is below 0
                    ((self.__last_snow_end_time is None) or ((self.__last_snow_end_time is not None) and (
                            current_time - self.__last_snow_end_time > self.__wait_time_until_next_snow))) and
                    random.randint(0, 100) <= 5):  # 5% of snow
                self.__is_snowing = True
                self.__snow_time = compute_snow_time()
                self.__snow_start_time = time.time()
                self.__last_snow_end_time = None
                self.__wait_time_until_next_snow = None

    def to_string(self):
        return (f"Weather: "
                f"\n- Current time: {time.time()}"
                f"\n- Current season: {self.__current_season}"
                f"\n- Last season changed time: {self.__last_season_changed_time}"
                f"\n- Is raining: {'Yes' if self.__is_raining else 'No'}"
                f"\n- Rain duration: {self.__rain_time}"
                f"\n- Rain start time: {self.__rain_start_time}"
                f"\n- Is snowing: {'Yes' if self.__is_snowing else 'No'}"
                f"\n- Snow duration: {self.__snow_time}"
                f"\n- Snow start time: {self.__snow_start_time}")
