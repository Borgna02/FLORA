from sensors.sensor import Sensor
import random
import time
from lib.utils import *

HEIGHT_RANGE = {
    MIN_THRESHOLD_KEY: 0.0,
    MAX_THRESHOLD_KEY: 60.0
}

WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_HEIGHT_IN_SECONDS = {
    MIN_THRESHOLD_KEY: 2,
    MAX_THRESHOLD_KEY: 4
}


def compute_wait_time_until_next_increment_of_height_density():
    return random.uniform(WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_HEIGHT_IN_SECONDS[MIN_THRESHOLD_KEY], WAIT_TIME_UNTIL_NEXT_INCREMENT_OF_HEIGHT_IN_SECONDS[MAX_THRESHOLD_KEY])

class UltrasonicSensor(Sensor):

    def __init__(self, environment):
        self.__current_height = HEIGHT_RANGE[MIN_THRESHOLD_KEY]
        self.__last_height_increment_time = time.time()
        self.__wait_time_until_next_increment_of_height = compute_wait_time_until_next_increment_of_height_density()
        super().__init__(environment)

    def read(self):
        if self.__current_height >= HEIGHT_RANGE[MAX_THRESHOLD_KEY]:
            return self.__current_height

        current_time = time.time()

        if (current_time - self.__last_height_increment_time) > self.__wait_time_until_next_increment_of_height:
            self.__last_height_increment_time = current_time
            self.__wait_time_until_next_increment_of_height = compute_wait_time_until_next_increment_of_height_density()

            if self.__current_height < HEIGHT_RANGE[MAX_THRESHOLD_KEY]:
                self.__current_height = min(self.__current_height + random.uniform(0, 1.0), HEIGHT_RANGE[MAX_THRESHOLD_KEY])

        return self.__current_height
