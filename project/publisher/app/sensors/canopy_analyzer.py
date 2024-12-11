from sensors.sensor import Sensor
import random
import time
from lib.utils import *

CANOPY_DENSITY_RANGE = {
    MIN_THRESHOLD_KEY: 0.0,
    MAX_THRESHOLD_KEY: 100.0
}

WAIT_TIME_UNTIL_CANOPY_DENSITY_CUT_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 180,
    MAX_THRESHOLD_KEY: 240
}

WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_CANOPY_DENSITY_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 1,
    MAX_THRESHOLD_KEY: 2
}


def compute_wait_time_until_canopy_density_cut():
    return random.uniform(WAIT_TIME_UNTIL_CANOPY_DENSITY_CUT_IN_SECONDS[MIN_THRESHOLD_KEY], WAIT_TIME_UNTIL_CANOPY_DENSITY_CUT_IN_SECONDS[MAX_THRESHOLD_KEY])

def compute_wait_time_until_next_increment_of_canopy_density():
    return random.uniform(WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_CANOPY_DENSITY_IN_SECONDS[MIN_THRESHOLD_KEY], WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_CANOPY_DENSITY_IN_SECONDS[MAX_THRESHOLD_KEY])

class CanopyAnalyzer(Sensor):

    def __init__(self, environment):
        self.__current_canopy_density = CANOPY_DENSITY_RANGE[MIN_THRESHOLD_KEY]
        current_time = time.time()
        self.__last_canopy_density_increment_time = current_time
        self.__wait_time_until_next_increment_of_canopy_density = compute_wait_time_until_next_increment_of_canopy_density()
        self.__last_canopy_density_cut_time = current_time
        self.__wait_time_until_canopy_density_cut = compute_wait_time_until_canopy_density_cut()
        super().__init__(environment)

    def read(self):
        current_time = time.time()

        if (current_time - self.__last_canopy_density_increment_time) > self.__wait_time_until_next_increment_of_canopy_density:
            self.__last_canopy_density_increment_time = current_time
            self.__wait_time_until_next_increment_of_canopy_density = compute_wait_time_until_next_increment_of_canopy_density()

            if (current_time - self.__last_canopy_density_cut_time) > self.__wait_time_until_canopy_density_cut:
                self.__current_canopy_density -= self.__current_canopy_density * random.uniform(0.3, 0.5)  # cut a percentage of the canopy between the 30% and the 50% of current canopy density
                self.__last_canopy_density_cut_time = current_time
                self.__wait_time_until_canopy_density_cut = compute_wait_time_until_canopy_density_cut()

            if self.__current_canopy_density < CANOPY_DENSITY_RANGE[MAX_THRESHOLD_KEY]:
                self.__current_canopy_density = min(self.__current_canopy_density + random.uniform(0.5, 2.0), CANOPY_DENSITY_RANGE[MAX_THRESHOLD_KEY])

        return self.__current_canopy_density
