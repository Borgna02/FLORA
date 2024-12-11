from sensors.sensor import Sensor


class TemperatureSensor(Sensor):

    def __init__(self, environment):
        super().__init__(environment)

    def read(self):
        return self.environment.current_temperature
