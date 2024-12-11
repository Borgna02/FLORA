from sensors.sensor import Sensor
import random
import time
from lib.utils import *

CHLOROPHYLL_CONTENT_RANGE = {
    MIN_THRESHOLD_KEY: 1.0,
    MAX_THRESHOLD_KEY: 150.0
}

WAIT_TIME_UNTIL_CHLOROPHYLL_CONTENT_CUT_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 30,
    MAX_THRESHOLD_KEY: 140
}

WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_CHLOROPHYLL_CONTENT_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 1,
    MAX_THRESHOLD_KEY: 2
}


def compute_wait_time_until_chlorophyll_content_cut():
    return random.uniform(WAIT_TIME_UNTIL_CHLOROPHYLL_CONTENT_CUT_IN_SECONDS[MIN_THRESHOLD_KEY],
                          WAIT_TIME_UNTIL_CHLOROPHYLL_CONTENT_CUT_IN_SECONDS[MAX_THRESHOLD_KEY])


def compute_wait_time_until_next_increment_of_chlorophyll_content():
    return random.uniform(WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_CHLOROPHYLL_CONTENT_IN_SECONDS[MIN_THRESHOLD_KEY],
                          WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_CHLOROPHYLL_CONTENT_IN_SECONDS[MAX_THRESHOLD_KEY])


class ChlorophyllFluorescenceSensor(Sensor):

    def __init__(self, environment):
        self.__current_chlorophyll_content = random.uniform(CHLOROPHYLL_CONTENT_RANGE[MIN_THRESHOLD_KEY], CHLOROPHYLL_CONTENT_RANGE[MAX_THRESHOLD_KEY])
        current_time = time.time()
        self.__last_chlorophyll_content_increment_time = current_time
        self.__wait_time_until_next_increment_of_chlorophyll_content = compute_wait_time_until_next_increment_of_chlorophyll_content()
        self.__last_chlorophyll_content_cut_time = current_time
        self.__wait_time_until_chlorophyll_content_cut = compute_wait_time_until_chlorophyll_content_cut()
        super().__init__(environment)

    def read(self):
        current_time = time.time()

        if (current_time - self.__last_chlorophyll_content_increment_time) > self.__wait_time_until_next_increment_of_chlorophyll_content:
            self.__last_chlorophyll_content_increment_time = current_time
            self.__wait_time_until_next_increment_of_chlorophyll_content = compute_wait_time_until_next_increment_of_chlorophyll_content()

            if (current_time - self.__last_chlorophyll_content_cut_time) > self.__wait_time_until_chlorophyll_content_cut:
                self.__current_chlorophyll_content -= self.__current_chlorophyll_content * random.uniform(0.3, 0.5)  # cut a percentage of the chlorophyll content the 30% and the 50% of current chlorophyll content
                self.__last_chlorophyll_content_cut_time = current_time
                self.__wait_time_until_chlorophyll_content_cut = compute_wait_time_until_chlorophyll_content_cut()

            if self.__current_chlorophyll_content < CHLOROPHYLL_CONTENT_RANGE[MAX_THRESHOLD_KEY]:
                self.__current_chlorophyll_content = min(self.__current_chlorophyll_content + random.uniform(0, 5), CHLOROPHYLL_CONTENT_RANGE[MAX_THRESHOLD_KEY])

        return self.__current_chlorophyll_content
