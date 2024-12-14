import paho.mqtt.client as mqtt
import time
import json
import random
from domain.environment import Environment
from sensors.temperature_sensor import TemperatureSensor
from sensors.ph_sensor import PHSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.canopy_analyzer import CanopyAnalyzer
from sensors.chlorophyll_fluorescence_sensor import ChlorophyllFluorescenceSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.generic_sensor import GenericSensor

ENVIRONMENT_KEY = "environment"
FARMS_KEY = "farms"
FARM_ID_KEY = "farm_id"
PLANT_KEY = "plant"
PLANT_ID_KEY = "plant_id"
SENSORS_KEY = "sensors"

# Configurazione del broker MQTT
BROKER = "mqtt_broker"  # Nome del servizio nel docker-compose.yml
PORT = 1883
TOPIC_STRUCTURE = "/farm_{farm_id}/plant_{plant_id}/{sensor_type}"  # Struttura del topic


def retrieve_sensor_data():
    with open('/app/sensors-config/sensors-config.json', 'r') as file:
        sensors_data = json.load(file)["sensors"]
        return [{'name': sensor["name"], 'boundaries': (sensor["min"], sensor["max"]), 'thresholds': (sensor["threshold_min"], sensor["threshold_max"])} for sensor in sensors_data]


def field_config():
    with open('/app/sensors-config/plants-config.json', 'r') as file:
        environment = Environment()
        configured_sensors = retrieve_sensor_data()
        farms = json.load(file)[FARMS_KEY]
        return {
            ENVIRONMENT_KEY: environment,
            FARMS_KEY: [
                {
                    FARM_ID_KEY:
                        farm[FARM_ID_KEY],
                    PLANT_KEY:
                        {
                            PLANT_ID_KEY: plant[PLANT_ID_KEY],
                            SENSORS_KEY:
                                {
                                    sensor_data['name']: handle_sensor_creation(sensor_data['name'], environment, sensor_data['boundaries'], sensor_data['thresholds'])
                                    for sensor_data in configured_sensors
                                }

                        }
                }
                for farm in farms for plant in farm["plants"]
            ]
        }


def handle_sensor_creation(sensor_name, environment, boundaries=None, thresholds=None):
    match sensor_name:
        case "temperature":
            return TemperatureSensor(environment)
        case "humidity":
            return HumiditySensor(environment)
        case "chlorophyll_content":
            return ChlorophyllFluorescenceSensor(environment)
        case "ph_level":
            return PHSensor(environment)
        case "height":
            return UltrasonicSensor(environment)
        case "canopy_density":
            return CanopyAnalyzer(environment)
        case _:
            return GenericSensor(boundaries, thresholds)


# Connessione al broker
client = mqtt.Client("Publisher")
client.connect(BROKER, PORT)


# Funzione per pubblicare dati su MQTT
def publish_data(field):
    environment = field[ENVIRONMENT_KEY]
    while True:
        environment.update()
        for plant in field[FARMS_KEY]:
            for sensor_type in plant[PLANT_KEY][SENSORS_KEY].keys():
                sensor = plant[PLANT_KEY][SENSORS_KEY][sensor_type]
                # Introduce some noise to simulate real-world variability
                noise = random.uniform(-0.5, 0.5)
                value = sensor.read() + noise
                payload = json.dumps({"value": value})  # Serializza solo il valore in JSON
                topic = TOPIC_STRUCTURE.format(farm_id=plant[FARM_ID_KEY], plant_id=plant[PLANT_KEY][PLANT_ID_KEY],
                                               sensor_type=sensor_type)
                client.publish(topic, payload)
        print(f"Published! {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}", flush=True)
        time.sleep(5)  # Attendi 5 secondi prima di inviare nuovi dati


if __name__ == "__main__":
    configured_field = field_config()
    publish_data(configured_field)
