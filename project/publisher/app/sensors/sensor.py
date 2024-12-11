from abc import ABC, abstractmethod


class Sensor(ABC):

    def __init__(self, environment):
        self.__environment = environment

    @property
    def environment(self):
        return self.__environment

    @abstractmethod
    def read(self):
        pass
